FROM alpine:latest

RUN apk --no-cache update && \
    apk --no-cache add python py-pip py-setuptools ca-certificates curl groff less bash && \
    pip --no-cache-dir install awscli && \
    rm -rf /var/cache/apk/*

COPY backup /etc/periodic/daily/backup

RUN chmod +x /etc/periodic/daily/backup

VOLUME ["/unifi"]

CMD ["crond", "-l", "2", "-f"]