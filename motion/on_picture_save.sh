#! /bin/bash

END_TIME=$(date +%s)

while getopts c:f: option ; do
    case "${option}" in
        c ) 
            CAMERA=${OPTARG}
            ;;
        f ) 
            PICTURE=${OPTARG}
            ;;
    esac
done

# ensure the directory for json files exists
mkdir -p /nvr/motion/events/${CAMERA}
# ensure the directory for preview images exists
mkdir -p /nvr/motion/preview/${CAMERA}

# replace the END_TIME placeholder
sed -i -e "s/END_TIME/${END_TIME}/g" /nvr/motion/events/${CAMERA}-*.json

# get the start time from the json file
start_time=$(jq -r '.start' < /nvr/motion/events/${CAMERA}-*.json)
# move the picture file and use the start time as the name
mv "${PICTURE}" /nvr/motion/preview/${CAMERA}/${start_time}.jpg

# move the json file now that it is valid
mv /nvr/motion/events/${CAMERA}-*.json /nvr/motion/events/${CAMERA}/

# rename the json file to remove teh camera id prefix
for file in /nvr/motion/events/${CAMERA}/${CAMERA}-*.json; do 
    mv "${file}" "${file/${CAMERA}-/}"
done

/usr/bin/mosquitto_pub -h mqtt -t cameras/${CAMERA}/motion -m 'OFF'