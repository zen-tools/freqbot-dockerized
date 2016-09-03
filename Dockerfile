FROM debian:jessie

MAINTAINER Dmitriy Poltavchenko <admin@linuxhub.ru>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python python-twisted python-simplejson python-regex vim locales

ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

RUN mkdir /chatlogs
RUN mkdir /var/log/freqbot/

ADD freqbot /opt/freqbot
RUN find /opt/freqbot -name '*.pyc' -delete

WORKDIR /opt/freqbot
CMD python start.py freqbot.conf
