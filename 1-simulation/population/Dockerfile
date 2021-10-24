FROM python:3.8

RUN mkdir /home/workdir
WORKDIR /home/workdir

COPY ./requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN git clone https://github.com/kornelro/matsim-python-tools.git
RUN pip install ./matsim-python-tools/.

COPY ./scripts/. .
COPY ./config/config.json .
COPY ./run.sh .
RUN chmod +rx ./run.sh

RUN mkdir data
RUN mkdir populations