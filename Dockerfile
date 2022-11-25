FROM python:3.8.13-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/django

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
