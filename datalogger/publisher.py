import os

import pika


def publish_message(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get("RABBITMQ_HOST"))
    )
    channel = connection.channel()

    queue_name = "log_data"
    exchange_name = "log_exchange"

    channel.exchange_declare(exchange=exchange_name, exchange_type="direct")

    channel.queue_declare(queue=queue_name)

    channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=queue_name)

    channel.basic_publish(exchange=exchange_name, routing_key=queue_name, body=message)

    connection.close()
