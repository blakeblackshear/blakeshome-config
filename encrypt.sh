#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ -z ${BLAKESHOME_PASS+x} ]; then 
    read -s -p "Password:" BLAKESHOME_PASS
    export BLAKESHOME_PASS
fi

/usr/bin/openssl enc -aes-256-cbc -salt -in $DIR/home-assistant/secrets.yaml -out $DIR/home-assistant/secrets.yaml.enc -pass env:BLAKESHOME_PASS
/usr/bin/openssl enc -aes-256-cbc -salt -in $DIR/DOCKER.env -out $DIR/DOCKER.env.enc -pass env:BLAKESHOME_PASS
