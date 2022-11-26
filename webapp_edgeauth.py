import binascii
import hashlib
import hmac
import optparse
import os
import re
import sys
import time
if sys.version_info[0] >= 3:
    from urllib.parse import quote_plus
else:
    from urllib import quote_plus
from flask import jsonify
import json

from flask import Flask, escape, request
import requests
import sys
import os
from flask import Flask, render_template, escape, request


# Force the local timezone to be GMT.
os.environ['TZ'] = 'GMT'

key = ''

class EdgeAuthError(Exception):
    def __init__(self, text):
        self._text = text

    def __str__(self):
        return 'EdgeAuthError:{0}'.format(self._text)

    def _getText(self):
        return str(self)
    text = property(_getText, None, None,
        'Formatted error text.')


class EdgeAuth:
    def __init__(self, token_type=None, token_name='__token__',
                 key=None, algorithm='sha256', salt=None,
                 ip=None, payload=None, session_id=None,
                 start_time=None, end_time=None, window_seconds=None,
                 field_delimiter='~', acl_delimiter='!',
                 escape_early=False, verbose=False):

        if key is None or len(key) <= 0:
            raise EdgeAuthError('You must provide a secret in order to '
                'generate a new token.')

        self.token_type = token_type
        self.token_name = token_name
        self.key = key
        self.algorithm = algorithm
        self.salt = salt
        self.ip = ip
        self.payload = payload
        self.session_id = session_id
        self.start_time = start_time
        self.end_time = end_time
        self.window_seconds = window_seconds
        self.field_delimiter = field_delimiter
        self.acl_delimiter = acl_delimiter
        self.escape_early = escape_early
        self.verbose = verbose

    def _escape_early(self, text):
        if self.escape_early:
            def toLower(match):
                return match.group(1).lower()
            return re.sub(r'(%..)', toLower, quote_plus(text))
        else:
            return text

    def _generate_token(self, path, is_url):
        start_time = self.start_time
        end_time = self.end_time

        if str(start_time).lower() == 'now':
            start_time = int(time.mktime(time.gmtime()))
        elif start_time:
            try:
                if int(start_time) <= 0:
                    raise EdgeAuthError('start_time must be ( > 0 )')
            except:
                raise EdgeAuthError('start_time must be numeric or now')

        if end_time:
            try:
                if int(end_time) <= 0:
                    raise EdgeAuthError('end_time must be ( > 0 )')
            except:
                raise EdgeAuthError('end_time must be numeric')

        if self.window_seconds:
            try:
                if int(self.window_seconds) <= 0:
                    raise EdgeAuthError('window_seconds must be ( > 0 )')
            except:
                raise EdgeAuthError('window_seconds must be numeric')

        if end_time is None:
            if self.window_seconds:
                if start_time is None:
                    # If we have a window_seconds without a start time,
                    # calculate the end time starting from the current time.
                    end_time = int(time.mktime(time.gmtime())) + \
                        self.window_seconds
                else:
                    end_time = start_time + self.window_seconds
            else:
                raise EdgeAuthError('You must provide an expiration time or '
                    'a duration window ( > 0 )')

        if start_time and (end_time <= start_time):
            raise EdgeAuthError('Token will have already expired.')

        if self.verbose:
            print('''
Akamai Token Generation Parameters
Token Type      : {0}
Token Name      : {1}
Key/Secret      : {2}
Algo            : {3}
Salt            : {4}
IP              : {5}
Payload         : {6}
Session ID      : {7}
Start Time      : {8}
End Time        : {9}
Window(seconds) : {10}
Field Delimiter : {11}
ACL Delimiter   : {12}
Escape Early    : {13}
PATH            : {14}
Generating token...'''.format(self.token_type if self.token_type else '',
                            self.token_name if self.token_name else '',
                            self.key if self.key else '',
                            self.algorithm if self.algorithm else '',
                            self.salt if self.salt else '',
                            self.ip if self.ip else '',
                            self.payload if self.payload else '',
                            self.session_id if self.session_id else '',
                            start_time if start_time else '',
                            end_time if end_time else '',
                            self.window_seconds if self.window_seconds else '',
                            self.field_delimiter if self.field_delimiter else '',
                            self.acl_delimiter if self.acl_delimiter else '',
                            self.escape_early if self.escape_early else '',
                            ('url: ' if is_url else 'acl: ') + path))

        hash_source = []
        new_token = []

        if self.ip:
            new_token.append('ip={0}'.format(self._escape_early(self.ip)))

        if start_time:
            new_token.append('st={0}'.format(start_time))

        new_token.append('exp={0}'.format(end_time))

        if not is_url:
            new_token.append('acl={0}'.format(path))

        if self.session_id:
            new_token.append('id={0}'.format(self._escape_early(self.session_id)))

        if self.payload:
            new_token.append('data={0}'.format(self._escape_early(self.payload)))

        hash_source = list(new_token)
        if is_url:
            hash_source.append('url={0}'.format(self._escape_early(path)))

        if self.salt:
            hash_source.append('salt={0}'.format(self.salt))

        if self.algorithm.lower() not in ('sha256', 'sha1', 'md5'):
            raise EdgeAuthError('Unknown algorithm')

        token_hmac = hmac.new(
            binascii.a2b_hex(self.key.encode()),
            self.field_delimiter.join(hash_source).encode(),
            getattr(hashlib, self.algorithm.lower())).hexdigest()
        new_token.append('hmac={0}'.format(token_hmac))

        return self.field_delimiter.join(new_token)

    def generate_acl_token(self, acl):
        if not acl:
            raise EdgeAuthError('You must provide acl')
        elif isinstance(acl, list):
            acl = self.acl_delimiter.join(acl)
        return self._generate_token(acl, False)

    def generate_url_token(self, url):
        if not url:
            raise EdgeAuthError('You must provide url')
        return self._generate_token(url, True)

'''
def genToken(inputJson):
    generator = EdgeAuth(
            token_type=inputJson['token_type'],
            token_name=inputJson['token_name'],
            key=inputJson['key'],
            algorithm=inputJson['algorithm'],
            salt=inputJson['salt'],
            ip=inputJson['ip_address'],
            payload=inputJson['payload'],
            session_id=inputJson['session_id'],
            start_time=inputJson['start_time'],
            end_time=inputJson['end_time'],
            window_seconds=inputJson['window_seconds'],
            field_delimiter=inputJson['field_delimiter'],
            acl_delimiter=inputJson['acl_delimiter'],
            escape_early=inputJson['escape_early'],
            verbose=inputJson['verbose'])

    url=inputJson['url']
    acl=inputJson['access_list']

    if (url and acl):
        print("You should input one in the 'url' or the 'acl'.")
    else:
        if acl:
            token = generator.generate_acl_token(acl)
        else: # url
            token = generator.generate_url_token(url)

        print("### Cookie or Query String ###")
        print("{0}={1}".format(options.token_name, token))
        print("### Header ###")
        print("{0}: {1}".format(options.token_name, token))
    return token
'''
def genToken(inputJson):
    generator = EdgeAuth(key=inputJson['key'],window_seconds=300,token_name=inputJson['token_name'])

    url = ''
    if 'url' in inputJson:
        url=inputJson['url']
    acl=inputJson['access_list']

    if (url and acl):
        print("You should input one in the 'url' or the 'acl'.")
    else:
        if acl:
            token = generator.generate_acl_token(acl)
        else: # url
            token = generator.generate_url_token(url)
    token = "{0}={1}".format(inputJson['token_name'], token)
    return token



app = Flask(__name__)


@app.route('/getToken')
def shorttoken():
    acl = request.args.get('acl')
    token = request.args.get('token_name')
    print(acl)
    print(token)
    inputJson = {}
    inputJson['access_list'] = acl
    inputJson['key'] = key
    inputJson['token_name'] = token
    token = genToken(inputJson)
    response = jsonify(token)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Short Token Gen Server')
    parser.add_argument('--key',required=True, default=None,help='Token ')
    args = parser.parse_args()
    key = args.key

    app.run()
