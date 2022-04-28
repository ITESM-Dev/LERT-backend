FROM python:3.10.4 as base
WORKDIR /usr/src/lert-backend

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps
RUN apt-get update
RUN pip install --upgrade pip

RUN pip install pipenv

COPY ./Pipfile .
RUN pipenv install
COPY . .

