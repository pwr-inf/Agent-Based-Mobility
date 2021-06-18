FROM python:3.7

USER root
RUN mkdir /home/workdir
WORKDIR /home/workdir

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update
RUN apt-get -y install curl
RUN apt-get install -y libspatialindex-dev
RUN git clone https://github.com/arup-group/genet.git
RUN pip install -e genet/.

RUN apt-get update -y
RUN apt-get install -y convmv

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir bash_scripts
COPY bash_scripts bash_scripts
RUN mkdir python_scripts
COPY python_scripts python_scripts
RUN mkdir config
COPY config config
COPY run.sh .
RUN chmod +rx run.sh
RUN chmod +rx bash_scripts/download_data.sh
RUN chmod +rx bash_scripts/process_data.sh
RUN chmod +rx bash_scripts/find_links.sh

RUN mkdir data