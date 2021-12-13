FROM tiagopeixoto/graph-tool

USER root
WORKDIR /home/workdir

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts ./scripts

RUN mkdir scenarios