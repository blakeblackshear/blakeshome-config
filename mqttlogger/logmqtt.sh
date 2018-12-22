#!/bin/sh

mosquitto_sub -h mqtt.blakeshome.com -v -t google/location/# -t network/dhcp/3c:28:6d:2a:f0:f4 -t network/dhcp/3c:28:6d:e3:ec:c4 -t location/# > /mqttlogger/mqtt_location.log