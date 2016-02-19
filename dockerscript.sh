#!/bin/bash
set -x
set -e

dnf install -y /usr/bin/spectool /usr/bin/rpmbuild /usr/bin/copr-cli /usr/bin/python3-config

useradd -u ${XUID:-1000} bob

mkdir -p /home/bob/rpmbuild/SOURCES

find . -maxdepth 1 -type f -exec cp -v '{}' /home/bob/rpmbuild/SOURCES ';'

spectool -C /home/bob/rpmbuild/SOURCES -g /work/boost.spec

chown -R bob: /home/bob

su - bob -c "rpmbuild -bs /work/boost.spec"

copr-cli --debug --config ./copr-config build boost /home/bob/rpmbuild/SRPMS/*.src.rpm
