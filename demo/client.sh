#!/bin/bash

# good user / crawler
curl -G 'localhost:8000/echo?salt=good1&nonce=cat&hash=4d60e90137b30d77d434cca7a74159441e4304157b72591c2d6cf8466d9a32bc'

# attacker with bad salt
curl -G 'localhost:8000/echo?salt=bad&nonce=cat&hash=0000000000000000000000000000000000000000000000000000000000000000'

# attacker with bad hash
curl -G 'localhost:8000/echo?salt=good1&nonce=cat&hash=F000000000000000000000000000000000000000000000000000000000000000'

# attacker with bad nonce
curl -G 'localhost:8000/echo?salt=good1&nonce=cat&hash=0000000000000000000000000000000000000000000000000000000000000000'


