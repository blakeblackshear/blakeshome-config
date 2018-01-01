#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ -z ${BLAKESHOME_PASS+x} ]; then 
    read -s -p "Password:" BLAKESHOME_PASS
    export BLAKESHOME_PASS
fi

/usr/bin/openssl enc -aes-256-cbc -d -salt -in $DIR/home-assistant/secrets.yaml.enc -out $DIR/home-assistant/secrets.yaml -pass env:BLAKESHOME_PASS
/usr/bin/openssl enc -aes-256-cbc -d -salt -in $DIR/DOCKER.env.enc -out $DIR/DOCKER.env -pass env:BLAKESHOME_PASS
