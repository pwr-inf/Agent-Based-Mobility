FROM python:3.7

USER root
RUN mkdir /home/workdir
WORKDIR /home/workdir

COPY ./requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update
RUN apt-get -y install curl
RUN apt-get install -y libspatialindex-dev
RUN git clone https://github.com/arup-group/genet.git
RUN pip install -e genet/.
RUN pip install -r requirements.txt

COPY ./scripts/. .
COPY ./run.sh .
RUN chmod +rx ./run.sh

RUN mkdir scenarios
RUN mkdir input_data