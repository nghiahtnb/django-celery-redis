FROM python:3.8.9-buster

# set work directory
WORKDIR /usr/src/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirement files
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


