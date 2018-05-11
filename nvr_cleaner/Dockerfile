FROM alpine:latest

COPY cleaner /etc/periodic/hourly/cleaner

RUN chmod +x /etc/periodic/hourly/cleaner

VOLUME ["/data"]

CMD ["crond", "-l", "2", "-f"]