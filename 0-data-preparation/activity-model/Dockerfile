FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install git -y

RUN mkdir /home/workdir
WORKDIR /home/workdir

COPY run.sh .
RUN chmod +rx run.sh

RUN mkdir data