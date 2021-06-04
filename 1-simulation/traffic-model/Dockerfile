FROM openjdk:11
RUN apt-get install unzip

USER root
RUN mkdir /home/workdir
WORKDIR /home/workdir

RUN curl -L -o ./matsim-13.zip https://github.com/matsim-org/matsim-libs/releases/download/13.0/matsim-13.0-release.zip
RUN unzip ./matsim-13.zip -d ./

COPY ./config/. .
COPY ./run.sh .
RUN chmod +rx ./run.sh

RUN mkdir data
RUN mkdir populations
RUN mkdir scenarios
RUN mkdir output