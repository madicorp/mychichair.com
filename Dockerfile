FROM python:3.5
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/mychichair

# Getting all project's dependencies
RUN apt-get update && apt-get install -y libpq-dev python3-dev
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get install nodejs
RUN apt-get purge -y curl
RUN npm i webpack -g

ADD ./package.json /usr/src/mychichair/package.json
RUN npm install

ADD ./requirements.txt /usr/src/mychichair/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /usr/src/mychichair/

RUN python manage.py collectstatic --noinput
RUN npm run build-assets
RUN cp -rf /usr/src/mychichair/mychichair/static/assets /usr/src/mychichair/static/assets
# Activate when compression will be used
# RUN DJANGO_SETTINGS_MODULE="mychichair.settings" SECRET_KEY="dummy_secret_to_compress" DEBUG="False" python manage.py compress

# Change the ownersihp of these directories as they are used during container execution
RUN mkdir -p /var/log/mychichair
RUN chown -R www-data:www-data /usr/src/mychichair
RUN chown -R www-data:www-data /var/log/mychichair
RUN mkdir -p /var/www
RUN chown -R www-data:www-data /var/www/
RUN chown -R www-data:www-data /usr/local/lib/python3.5/
# Change user to run the rest of the image build and to run the container
USER www-data
