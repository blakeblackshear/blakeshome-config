#!/bin/sh

op="${1:-op}"
mac="${2:-mac}"
ip="${3:-ip}"
hostname="${4}"

tstamp="`date '+%s'`"

topic="network/dhcp/${mac}"
payload="${tstamp}"

mosquitto_pub -h mqtt.blakeshome.com -t "${topic}" -m "${payload}" -r