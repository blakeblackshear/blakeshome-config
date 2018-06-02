FROM alpine:latest

RUN apk --no-cache update && \
    apk --no-cache add python py-pip py-setuptools ca-certificates curl groff less bash openssl && \
    pip --no-cache-dir install awscli && \
    rm -rf /var/cache/apk/*

COPY backup /etc/periodic/hourly/backup

RUN chmod +x /etc/periodic/hourly/backup

VOLUME ["/unifi"]

CMD ["crond", "-l", "2", "-f"]