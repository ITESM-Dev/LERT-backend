FROM debian:7.6

RUN pip3.8 install pipenv==2021.11.9
WORKDIR /usr/src/lert-backend

COPY ./Pipfile .
RUN pipenv install

RUN chmod +x /cmd.sh
COPY cmd.sh / 

