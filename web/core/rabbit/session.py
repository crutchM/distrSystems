import pika

from os import getenv

CONNECTION = f'amqp://{getenv("RABBITMQ_DEFAULT_USER")}:{getenv("RABBITMQ_DEFAULT_PASS")}@{getenv("BROKER_HOST")}:5672/%2F'

QUEUE_NAME = getenv('QUEUE_NAME')

connection = pika.BlockingConnection(pika.URLParameters(CONNECTION))


def publish(message: str):
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message.encode('utf-8'))
    channel.close()