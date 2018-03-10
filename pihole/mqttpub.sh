#!/bin/sh

op="${1:-op}"
mac="${2:-mac}"
ip="${3:-ip}"
hostname="${4}"

# dont report on deleted leases
if [ $op = "del" ]
then
    exit 0
fi

tstamp="`date '+%s'`"

topic="network/dhcp/${mac}"

payload=$(cat <<EOF
{"op": "$op","timestamp": $tstamp}
EOF
)

mosquitto_pub -h mqtt.blakeshome.com -t "${topic}" -m "${payload}" -r