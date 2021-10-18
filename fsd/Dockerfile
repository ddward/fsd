FROM python:3.6
WORKDIR /fsd
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./ /fsd
CMD ["uwsgi","/fsd/api/api_uwsgi.ini"]
