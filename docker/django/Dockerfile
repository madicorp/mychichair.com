FROM python:3.4.5

RUN mkdir /usr/src/mychichair
WORKDIR /usr/src/mychichair

# Copy requirements to use docker layers cache if not changed
ADD ./requirements.txt /usr/src/mychichair/requirements.txt

# Getting all project's dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

ADD ./docker/django /usr/src/mychichair/docker/django

ADD ./mychichair/ /usr/src/mychichair/mychichair
ADD ./manage.py/ /usr/src/mychichair/manage.py
