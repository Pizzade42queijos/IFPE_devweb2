from confluent_kafka import Consumer, KafkaError
import smtplib
from email.mime.text import MIMEText
import json
import logging
import os

consumer = Consumer({ #consumidor
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka1:19091,kafka2:19092,kafka3:19093'),
    'group.id': 'notificador-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['notificacao'])

#Função para enviar o email
def send_email(file_name, operation):
    sender_email = os.getenv('devwebdois@gmail.com')
    recipient_email = os.getenv('audemarioalves@gmail.com')
    subject = "Operação Realizada!! VEJA!!!"
    body = f"O arquivo {file_name} foi {operation}." #não manda direito so ponto o nome

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, os.getenv('12345678910Ab'))
            server.send_message(msg)
            logging.info(f"E-mail enviado para {recipient_email}.")
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")

#kafka
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        elif not msg.error():
            data = json.loads(msg.value())
            file_name = data['file']
            operation = data['operation']
            send_email_notification(file_name, operation)
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            logging.error(f"Erro: {msg.error().str()}")

except KeyboardInterrupt: #não sei
    pass
finally:
    consumer.close()