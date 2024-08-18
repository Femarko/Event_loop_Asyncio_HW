FROM python:3.10-alpine

COPY ./requirements.txt .
RUN apk add --no-cache bash postgresql-client build-base postgresql-dev
RUN pip install -r requirements.txt

COPY . .
WORKDIR .


