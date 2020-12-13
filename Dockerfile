FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential python-dev
RUN python -m pip install uwsgi

COPY ./requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY ./data.db ./data.db
COPY ./uwsgi.ini ./uwsgi.ini

COPY ./movie_rankings ./

CMD ["uwsgi", "uwsgi.ini"]
