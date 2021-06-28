FROM nginx:stable-alpine

COPY steuerlotse.conf /etc/nginx/conf.d/default.conf

ARG UWSGI_HOST=web
RUN sed -i "s/web/${UWSGI_HOST}/" /etc/nginx/conf.d/default.conf
