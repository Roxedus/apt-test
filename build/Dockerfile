FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive CC=${DEB_HOST_GNU_TYPE}-gcc

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        binutils-aarch64-linux-gnu \
        build-essential \
        ca-certificates \
        curl \
        debhelper \
        dh-modaliases \
        dpkg \
        dpkg-dev \
        execstack \
        gcc-arm-linux-gnueabihf \
        python3 \
        python3-dev \
        python3-pip && \
    pip3 install jinja2 requests

COPY / scripts/

RUN chmod -x -R /scripts

ENTRYPOINT ["python3", "-u", "/scripts/gen_pack.py"]