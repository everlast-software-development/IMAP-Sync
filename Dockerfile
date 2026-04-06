## Root Dockerfile for Coolify / Docker Hub / CI (Nixpacks detects this and uses Docker build).
## Based on INSTALL.d/Dockerfile — paths adjusted for repository root.

FROM debian:bullseye

LABEL maintainer="Gilles LAMIRAL <gilles@lamiral.info>" \
      description="Imapsync" \
      documentation="https://imapsync.lamiral.info/#doc"

COPY Dockerfile imapsync INSTALL.d/prerequisites_imapsync /

RUN set -xe && \
  apt-get update \
  && apt-get install -y \
  libauthen-ntlm-perl \
  libcgi-pm-perl \
  libcrypt-openssl-rsa-perl \
  libcrypt-openssl-pkcs12-perl \
  libdata-uniqid-perl \
  libencode-imaputf7-perl \
  libfile-copy-recursive-perl \
  libfile-tail-perl \
  libio-compress-perl \
  libio-socket-ssl-perl \
  libio-socket-inet6-perl \
  libio-tee-perl \
  libhtml-parser-perl \
  libjson-webtoken-perl \
  libmail-imapclient-perl \
  libparse-recdescent-perl \
  libmodule-scandeps-perl \
  libpar-packer-perl \
  libproc-processtable-perl \
  libreadonly-perl \
  libregexp-common-perl \
  libsys-meminfo-perl \
  libterm-readkey-perl \
  libtest-mockobject-perl \
  libtest-pod-perl \
  libunicode-string-perl \
  liburi-perl \
  libwww-perl \
  procps \
  wget \
  make \
  cpanminus \
  lsof \
  ncat \
  openssl \
  ca-certificates \
  && rm -rf /var/lib/apt/lists/* \
  && cpanm IO::Socket::SSL

RUN set -xe \
  && cd /usr/bin/ \
  && wget -N --no-check-certificate https://imapsync.lamiral.info/imapsync \
        https://imapsync.lamiral.info/prerequisites_imapsync \
        https://raw.githubusercontent.com/google/gmail-oauth2-tools/master/python/oauth2.py \
  && chmod +x imapsync oauth2.py

USER nobody:nogroup

ENV HOME=/var/tmp/

WORKDIR /var/tmp/

STOPSIGNAL SIGINT

CMD ["/usr/bin/imapsync"]
