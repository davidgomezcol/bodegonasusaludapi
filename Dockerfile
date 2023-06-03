FROM python:3.10.3-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/django

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN apt-get upgrade -y && apt-get update -y && apt-get install gcc -y

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000
EXPOSE 5678
