# Token Auth at Player Side
This repo is an implementation of how to integrate the hls video player and token generation from python server and using the token to play back the content.

![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/tokenauthworkflow.jpg)

### Installation of Dependencies
```
$pip install -r requirements.txt
```

# Step 1: Token Auth in Delivery Config.

Set up the Segmented Media Protection Behavior in the delivery config and make a note of the key.

![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/smp.jpg)

# Step 2: HTTP Server Running.

Now, lets set up a Flask based python server that will listen on port 5000. This server on getting requests on path /getToken will generate the short token. This server has already the key configured in the delivery config.

![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/server.jpg)

# Step 3:  Integrate Token Fetching into the player's logic.

Integrate a HLS video player using videojs library in an HTML Page. This page takes the url and gets the token from the server which we setup.

### Without Token
![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/withouttoken.jpg)

### With Token
![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/tokencall.jpg)
![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/shorttoken.jpg)
![alt text1](https://github.com/Achuthananda/TokenAuthImplementation/blob/master/lontoken.jpg)
