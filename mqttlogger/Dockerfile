FROM debian:stretch-slim

RUN apt-get update && \
    apt-get install -y mosquitto-clients && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY . .

CMD [ "sh", "logmqtt.sh" ]