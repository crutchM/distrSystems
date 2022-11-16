import json
import sys
from os import getenv
import requests

import pika

USER = getenv("RABBITMQ_DEFAULT_USER") or "postrgres"
PASSWORD = getenv("RABBITMQ_DEFAULT_PASS") or "password"
BROKER_HOSTNAME = 'rabbit'
WEB_HOSTNAME = 'nginx'



CONNECTION_URL = 'amqp://user:password@rabbit:5672/%2F'

QUEUE_NAME = 'links'

def handle_message(ch, method, properties, body):
    body_str = body.decode('utf-8')
    link_json = json.loads(body_str)
    response = requests.get(link_json['url'], timeout=10)
    status = response.status_code
    payload = {'id': int(link_json['id']), 'status': str(status)}
    payload_json = json.dumps(payload)
    result = requests.put(f'http://{WEB_HOSTNAME}:80/links/', data=payload_json)
    print(result.content)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(CONNECTION_URL))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME, auto_ack=True, on_message_callback=handle_message)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)