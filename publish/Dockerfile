FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        ca-certificates \
        curl \
        debhelper \
        dpkg \
        gnupg2 \
        reprepro

COPY /entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]