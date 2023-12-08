FROM python:3.11-slim-buster
LABEL maintainer="Min"

WORKDIR /app
COPY ./ /app

RUN apt-get update && \
  apt-get install -y libzbar0 libgeos-dev build-essential libssl-dev libffi-dev python3-dev pkg-config && \
  pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

CMD ["gunicorn" , "-b", "0.0.0.0:8000", "app:app"]