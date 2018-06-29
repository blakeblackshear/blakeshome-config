#! /bin/bash

END_TIME=$(date +%s)

while getopts c: option ; do
    case "${option}" in
        c ) 
            CAMERA=${OPTARG}
            ;;
    esac
done

mkdir -p /nvr/motion/events/${CAMERA}

sed -i -e "s/END_TIME/${END_TIME}/g" /nvr/motion/events/${CAMERA}-*.json

mv /nvr/motion/events/${CAMERA}-*.json /nvr/motion/events/${CAMERA}/

for file in /nvr/motion/events/${CAMERA}/${CAMERA}-*.json; do mv "${file}" "${file/${CAMERA}-/}"; done

/usr/bin/mosquitto_pub -h mqtt -t cameras/${CAMERA}/motion -m 'OFF'