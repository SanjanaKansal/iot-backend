import json
import os
import pika

from datalogger.helpers import sanitise_electrical_data
from datalogger.serializers import ElectricalDataSerializer


def callback(ch, method, properties, body):
    body_content = json.loads(body)
    for data in body_content:
        serializer = ElectricalDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=serializer.validated_data)

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.environ.get("RABBITMQ_HOST"), port=int(os.environ.get("RABBITMQ_PORT"))
    ))
    channel = connection.channel()

    queue_name = 'log_data'
    exchange_name = 'log_exchange'

    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


start_consuming()
