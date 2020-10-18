FROM python:3.8.1-slim-buster

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /home/app/
