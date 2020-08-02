FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        curl \
        ca-certificates \
        dpkg \
        libicu-dev \
        tar \
        libcurl4-openssl-dev \
        libunwind8