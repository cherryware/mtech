FROM python:3.12.0-alpine3.18

ENV PIP_ROOT_USER_ACTION=ignore
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache libpq-dev build-base

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN mkdir /app

RUN adduser -u 1234 --disabled-password --gecos "" --no-create-home appuser && chown -R appuser /app
USER appuser

WORKDIR /app