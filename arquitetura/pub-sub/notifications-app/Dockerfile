# using a python small basic image
FROM python:3.8.13-alpine3.15

# creates a dir for our application
WORKDIR /notifications-app

RUN apk add zlib-dev jpeg-dev gcc musl-dev librdkafka-dev

RUN apk add --no-cache \
    gcc \
    musl-dev \
    librdkafka-dev \
    libffi-dev \
    openssl-dev

# copy our requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV KAFKA_BOOTSTRAP_SERVERS=kafka1:19091,kafka2:19092,kafka3:19093
ENV SENDER_EMAIL=devwebdois@gmail.com
ENV EMAIL_PASSWORD=123456789010AB
ENV RECIPIENT_EMAIL=audemarioalves@gmail.com

# Comando para iniciar a aplicação
CMD ["python", "notifications.py"]

# copy the rest of our application
COPY . .
# run the application
CMD python app.py