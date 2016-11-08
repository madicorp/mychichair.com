FROM tutum/nginx

RUN rm /etc/nginx/sites-enabled/default
ADD docker/nginx/sites-enabled/ /etc/nginx/sites-enabled
COPY ./index.html /usr/share/nginx/html
ADD ./js/ /usr/share/nginx/html/js
ADD ./images/ /usr/share/nginx/html/images
ADD ./fonts/ /usr/share/nginx/html/fonts
ADD ./css/ /usr/share/nginx/html/css

