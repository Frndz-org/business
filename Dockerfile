FROM python:3.11.8-slim
LABEL authors="9r1nd"

COPY . /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTCODE 1

ENV PYTHONUNBUFFERED 1

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh && chmod +x celery_entrypoint.sh
