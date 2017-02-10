#!/bin/bash

BASEDIR=$(dirname "$0")
if [ -z ${DATABASE_URL+x} ]; then
    echo "Making the migrations against sqlite"
    python manage.py makemigrations && python manage.py migrate --noinput
else
    echo "Waiting for connection before making the migrations"
    waitforit --host=db --port=5432 --timeout=15 && waitforit --host=redis --port=6379 --timeout=10\
    && python manage.py makemigrations && python manage.py migrate --noinput
fi

if [ -z ${POPULATE_DB+x} ]; then
    echo "Not populating the DB"
else
    python manage.py populatedb
fi

python manage.py install_site

if [ -z ${DATABASE_URL+x} ]; then
python manage.py runserver 0.0.0.0:8000
else
gunicorn mychichair.wsgi --bind 0.0.0.0:8000
fi
