FROM python:3.11.1-slim-bullseye
RUN apt update && apt install -y build-essential

RUN mkdir /app
WORKDIR /app

# add requirements.txt and startup scripts to the image
COPY requirements.txt /app/

# check if we have known security issues (CVE) in the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN python manage.py runserver 0.0.0.0:8080
