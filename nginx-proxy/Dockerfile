FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY uwsgi_params /etc/nginx/uwsgi_params
RUN rm /etc/nginx/conf.d/default.conf
EXPOSE  5051