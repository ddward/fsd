FROM alpine:3.14
RUN apk --no-cache add curl
RUN apk add --no-cache --upgrade bash
WORKDIR /
COPY test.sh test.sh
CMD ["bash", "test.sh"]