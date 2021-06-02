FROM kornelro/urban-mobility-project

RUN mkdir /home/workdir
WORKDIR /home/workdir

COPY scripts .
COPY run.sh .
RUN chmod +rx ./run.sh

RUN mkdir scenarios
RUN mkdir results
RUN mkdir data