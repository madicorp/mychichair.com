FROM python:3.4.5

RUN mkdir /usr/src/mychichair
WORKDIR /usr/src/mychichair

ADD ./requirements.txt /usr/src/mychichair/requirements.txt
# Copy requirements before to use docker layers' cache if not changed
RUN pip install --upgrade pip && pip install -r requirements.txt

ADD ./docker/mychichair/docker-entrypoint.sh /usr/src/mychichair/docker-entrypoint.sh

ADD ./mychichair/ /usr/src/mychichair/mychichair
ADD ./manage.py/ /usr/src/mychichair/manage.py
