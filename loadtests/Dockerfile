FROM python:3.12-slim

WORKDIR /loadtests

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["locust"]
