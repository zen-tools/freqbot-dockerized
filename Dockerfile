FROM debian:jessie

MAINTAINER Dmitriy Poltavchenko <admin@linuxhub.ru>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python python-twisted python-simplejson python-regex vim locales

ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

RUN mkdir /data
RUN mkdir /var/log/freqbot/
RUN chmod 777 /var/log/freqbot

ADD freqbot /opt/freqbot
RUN find /opt/freqbot -name '*.pyc' -delete
RUN python -mcompileall /opt/freqbot

WORKDIR /opt/freqbot
CMD python start.py freqbot.conf
