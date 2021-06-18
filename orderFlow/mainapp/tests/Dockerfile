FROM python:3.8.10-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/orderFlow

ENTRYPOINT python3 manage.py test
