FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /bingo

WORKDIR /bingo

ADD . /bingo/

RUN pip install -r requirements.txt
