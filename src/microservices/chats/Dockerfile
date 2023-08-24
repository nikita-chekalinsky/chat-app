# FROM --platform=linux/amd64 python:3.11
FROM python:3.11

RUN mkdir /app
WORKDIR /app
COPY microservices/chats/requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY microservices/chats/app /app
COPY libs/ ./libs/

RUN adduser --disabled-login appuser
USER appuser

ENV PYTHONPATH "${PYTHONPATH}:/app/libs"

CMD uvicorn app.main:app --host 0.0.0.0 --port $ECS_PORT