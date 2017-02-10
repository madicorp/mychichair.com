FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/mychichair

# Getting the project's dependencies
# We need the packages for python dependencies
RUN apk update && apk upgrade &&\
    apk add --no-cache gcc g++ libpq python3-dev postgresql-dev libffi-dev libxml2-dev libxslt-dev linux-headers \
    openssl libjpeg-turbo-dev

COPY ./requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apk add bash
ENV WAITFORIT_VERSION="v1.3.1"
RUN wget -q -O /usr/local/bin/waitforit https://github.com/maxcnunes/waitforit/releases/download/$WAITFORIT_VERSION/waitforit-linux_amd64 \
    && chmod +x /usr/local/bin/waitforit

COPY ./docker ./docker
COPY ./build/static/assets ./static/assets
COPY ./templates ./templates
COPY ./mychichair ./mychichair
COPY ./Procfile ./
COPY ./manage.py ./
COPY ./webpack.config.js ./
COPY ./build/static/webpack-bundle.json ./

RUN python manage.py collectstatic --noinput &&\
    DJANGO_SETTINGS_MODULE="mychichair.settings" SECRET_KEY="dummy_secret_to_compress" DEBUG="False" python manage.py compress

# ADD and COPY do not respect USER instruction and just set ownership to root thus this chown
RUN set -x ; addgroup -g 82 -S www-data ; adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1
RUN chown -R www-data:www-data /usr/local/lib/python3.5/
RUN chown -R www-data:www-data /usr/src/mychichair
RUN mkdir -p /var/log/mychichair && chown -R www-data:www-data /var/log/mychichair
RUN mkdir -p /var/www && chown -R www-data:www-data /var/www/
RUN mkdir -p /var/log/mychichair
RUN mkdir -p /var/www

# Change user to run the rest of the image build and to run the container
USER www-data
