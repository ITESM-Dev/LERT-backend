FROM python:3.10.4 as base
WORKDIR /usr/src/LERT-backend

# Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update && pip install --upgrade pip && pip install pipenv

COPY ./Pipfile .
RUN pipenv install

COPY . .
