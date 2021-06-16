FROM python:3.9

USER root
RUN mkdir /home/workdir
WORKDIR /home/workdir

RUN apt-get update -y
RUN apt-get install -y convmv

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir bash_scripts
COPY bash_scripts bash_scripts
RUN mkdir python_scripts
COPY python_scripts python_scripts
COPY run.sh .
RUN chmod +rx run.sh

RUN mkdir data