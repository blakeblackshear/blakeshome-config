#! /bin/bash

START_TIME=$(date +%s)

while getopts c:w:h:x:y: option ; do
    case "${option}" in
        c ) 
            CAMERA=${OPTARG}
            ;;
        w ) 
            WIDTH=${OPTARG}
            ;;
        h ) 
            HEIGHT=${OPTARG}
            ;;
        x ) 
            POS_X=${OPTARG}
            ;;
        y ) 
            POS_Y=${OPTARG}
            ;;
    esac
done

mkdir -p /nvr/motion/events/

cat <<EOF > /nvr/motion/events/${CAMERA}-${START_TIME}.json
{"start": ${START_TIME}, "end": END_TIME, "width": $WIDTH, "height": $HEIGHT, "x": $POS_X, "y": $POS_Y}
EOF

/usr/bin/mosquitto_pub -h mqtt -t cameras/${CAMERA}/motion -m 'ON'
