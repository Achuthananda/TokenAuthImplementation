# Akamai Token Authentication
Akamai Token Authentication is the process of generating tokens, associating them with an authenticated user session, and then validating the stream using these tokens to prevent unauthorized sharing of links to your content. You can read more about Token Auth [here](https://techdocs.akamai.com/adaptive-media-delivery/docs/add-token-auth).

This repo is an implementation of how to integrate the hls video player and Akamai token generation from python server and using the token to play back the content.


![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/images/tokenauthworkflow.jpg)

### Installation of Dependencies
```
$pip install -r requirements.txt
```

# Step 1: Token Auth in Delivery Config.

Set up the Segmented Media Protection Behavior in the delivery config and make a note of the key.

![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/images/smp.jpg)

# Step 2: HTTP Server Running.

Now, lets set up a Flask based python server that will listen on port 5000. This server on getting requests on path /getToken will generate the short token. This server has already the key configured in the delivery config.

![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/images/server.jpg)

# Step 3:  Integrate Token Fetching into the player's logic.

Integrate a HLS video player using videojs library in an HTML Page. This page takes the url and gets the token from the server which we setup.

### Without Token
![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/images/withouttoken.jpg)



### With Token
First token will be fetched from the token server
![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/images/tokencall.jpg)

Next master manifest will be requested using the short token
![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/images/shorttoken.jpg)

The urls of the child manifest and segments will be having long token in the url
![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/images/lontoken.jpg)
