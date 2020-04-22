FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc nginx supervisor
RUN python -m pip install uwsgi

COPY ./requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY ./movie_rankings ./

COPY ./uwsgi.ini ./uwsgi.ini
COPY ./data.db ./data.db
COPY ./nginx.conf /etc/nginx/sites-enabled/default
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord"]