FROM python:3.6
WORKDIR /fsd
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./fsd /fsd
EXPOSE 49152
CMD ["uwsgi","/fsd/main/api/api_uwsgi.ini"]