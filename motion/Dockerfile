FROM motionproject/motion:latest

RUN export DEBIAN_FRONTEND=noninteractive; \
    export DEBCONF_NONINTERACTIVE_SEEN=true; \
    apt-get update -qqy && apt-get install -qqy --option Dpkg::Options::="--force-confnew" --no-install-recommends \
    mosquitto-clients jq && \
    apt-get --quiet autoremove --yes && \
    apt-get --quiet --yes clean && \
    rm -rf /var/lib/apt/lists/*

COPY on_event_start.sh /on_event_start.sh
COPY on_picture_save.sh /on_picture_save.sh

RUN chmod +x /on_*.sh

VOLUME ["/data", "/usr/local/etc/motion"]
