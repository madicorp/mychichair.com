FROM tutum/nginx

RUN apt-get update

RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled

ADD nginx.conf /etc/nginx/nginx.conf

RUN chmod -R g+w /var/lib/nginx
RUN chgrp -R www-data var/lib/nginx/
RUN usermod -a -G www-data root
USER www-data
