#!/bin/bash

BASEDIR=$(dirname "$0")
if [ -z ${POSTGRES_1_PORT_5432_TCP_ADDR+x} ]; then
python manage.py makemigrations && python manage.py migrate --noinput && python manage.py createadmin \
&& python manage.py runserver 0.0.0.0:8000
else
$BASEDIR/wait-for-it.sh "$POSTGRES_1_PORT_5432_TCP_ADDR:$POSTGRES_1_PORT_5432_TCP_PORT" && \
$BASEDIR/wait-for-it.sh "$MYCHICHAIR_REDIS_1_PORT_5634_TCP_ADDR:$MYCHICHAIR_REDIS_1_PORT_5634_TCP_PORT" && \
python manage.py makemigrations && python manage.py migrate --noinput && python manage.py createadmin \
&& gunicorn mychichair.wsgi --bind 0.0.0.0:8000
fi