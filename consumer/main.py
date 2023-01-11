import json
import sys
from os import getenv
from typing import Optional

import requests
from redis import Redis
import pika

WEB_HOSTNAME = getenv('WEB_HOSTNAME')
WEB_PORT = getenv('WEB_PORT')

CACHE_HOSTNAME = getenv('CACHE_HOSTNAME')
CACHE_PORT = getenv('CACHE_PORT')

CONNECTION = f'amqp://{getenv("RABBITMQ_DEFAULT_USER")}:{getenv("RABBITMQ_DEFAULT_PASS")}@{getenv("BROKER_HOST")}:5672/%2F'
QUEUE_NAME = getenv('QUEUE_NAME')

redis_cache = Redis(host=CACHE_HOSTNAME, port=int(CACHE_PORT), db=0)


def get_link_status(link: str) -> str:
    key = f"url-{link}"
    status = get_status_from_cache(key)
    if status is None:
        status = fetch_status_from_inet(link)
        update_status_in_cache(key, status)
    return status


def get_status_from_cache(key: str) -> Optional[str]:
    value = redis_cache.get(key)
    return None if value is None else value.decode("utf-8")


def update_status_in_cache(key: str, status_code: str) -> None:
    redis_cache.set(name=key, value=status_code)


def fetch_status_from_inet(link: str) -> str:
    response = requests.get(link, timeout=10)
    status = str(response.status_code)
    return status


def handle_message(ch, method, properties, body):
    body_str = body.decode('utf-8')
    link_json = json.loads(body_str)
    status = get_link_status(link_json['url'])
    payload = {'id': int(link_json['id']), 'status': str(status)}
    payload_json = json.dumps(payload)
    result = requests.put(f'http://{WEB_HOSTNAME}:{WEB_PORT}/links/', data=payload_json)
    print(result.content)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(CONNECTION))
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