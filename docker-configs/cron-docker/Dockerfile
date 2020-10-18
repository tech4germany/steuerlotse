FROM alpine:3.6

COPY cronjobs /etc/crontabs/root

RUN apk --no-cache add curl

CMD ["crond", "-f", "-d", "8"]