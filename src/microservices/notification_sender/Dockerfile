FROM python:3.11.3


RUN mkdir /app
WORKDIR /app
COPY microservices/notification_sender/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY microservices/notification_sender/ ./
COPY libs/ ./libs/

RUN adduser --disabled-login appuser
USER appuser

ENV PYTHONPATH "${PYTHONPATH}:/app/libs"


CMD ["python", "main.py"]