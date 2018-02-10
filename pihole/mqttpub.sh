#!/bin/sh

op="${1:-op}"
mac="${2:-mac}"
ip="${3:-ip}"
hostname="${4}"

tstamp="`date '+%Y-%m-%d %H:%M:%S'`"

topic="network/dhcp/${mac}"
payload="${ip}-${hostname}"

mosquitto_pub -h mqtt.blakeshome.com -t "${topic}" -m "${payload}"