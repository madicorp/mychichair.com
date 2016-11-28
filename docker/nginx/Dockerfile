FROM tutum/nginx

RUN rm /etc/nginx/sites-enabled/default
ADD docker/nginx/sites-enabled/ /etc/nginx/sites-enabled
RUN rm /etc/nginx/nginx.conf
ADD docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./index.html /usr/share/nginx/html
ADD ./js/ /usr/share/nginx/html/js
ADD ./images/ /usr/share/nginx/html/images
ADD ./fonts/ /usr/share/nginx/html/fonts
ADD ./css/ /usr/share/nginx/html/css

RUN chmod -R g+w /var/lib/nginx
RUN chgrp -R www-data var/lib/nginx/
RUN usermod -a -G www-data root
USER www-data
