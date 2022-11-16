import pika


CONNECTION = 'amqp://user:password@rabbit:5672/%2F'

QUEUE_NAME = 'links'


def publish(message: str):
    connection = pika.BlockingConnection(pika.URLParameters(CONNECTION))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message.encode('utf-8'))
    channel.close()
    connection.close()