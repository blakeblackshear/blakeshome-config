FROM alpine:3.7

RUN apk add motion --update-cache --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted
RUN apk add bash mosquitto-clients jq --no-cache

COPY on_event_start.sh /on_event_start.sh
COPY on_event_end.sh /on_event_end.sh
COPY on_picture_save.sh /on_picture_save.sh

RUN chmod +x /on_*.sh

VOLUME ["/data", "/etc/motion"]

CMD [ "motion" ]