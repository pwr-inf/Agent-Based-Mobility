FROM openjdk:11
RUN apt-get install unzip

USER root
RUN mkdir /home/workdir
WORKDIR /home/workdir

# RUN curl -L -o ./matsim-13.zip https://github.com/matsim-org/matsim-libs/releases/download/13.0/matsim-13.0-release.zip
# RUN unzip ./matsim-13.zip -d ./

RUN curl -L -o ./pt2matsim-20-12.jar https://repo.matsim.org/repository/matsim/org/matsim/pt2matsim/21.5/pt2matsim-21.5-shaded.jar

RUN mkdir ./data
RUN mkdir bash_scripts
COPY bash_scripts bash_scripts
RUN mkdir ./config
COPY config config
COPY run.sh .
RUN chmod +rx run.sh