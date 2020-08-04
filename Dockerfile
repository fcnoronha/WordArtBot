FROM python:3.8

WORKDIR /app
ADD requirements.txt /app

RUN apt-get update -y
RUN apt-get install -y wkhtmltopdf

RUN pip3 install -r requirements.txt
ADD . /app
