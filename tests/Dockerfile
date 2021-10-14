FROM python:3.7-slim-buster
RUN apt-get update; apt-get install bash curl -y
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY test.sh test.sh
COPY test.py test.py
CMD ["bash", "test.sh"]