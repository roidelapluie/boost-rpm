FROM centos:7

MAINTAINER Julien Pivotto <roidelapluie@inuits.eu>

RUN mkdir /workspace
COPY . /workspace

RUN yum install -y /usr/bin/spectool /usr/bin/rpmbuild /usr/bin/yum-builddep


RUN useradd bob
RUN mkdir -p /home/bob/rpmbuild/SOURCES



RUN spectool -C /home/bob/rpmbuild/SOURCES -g /workspace/.spec
RUN yum-builddep -y /workspace/.spec

RUN chown -R bob: /home/bob /workspace

RUN su - bob -c "rpmbuild -ba /workspace/.spec"

VOLUME /artifacts
