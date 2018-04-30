import pika
import time
from threading import Thread

HOST = 'amqp://localhost'
EXCHANGE = 'goras_exchange'

class RmqInterface(object):
    def __init__(self, host=HOST, exchange=EXCHANGE):
        self.parameters = pika.URLParameters(host)
        self.exchange = exchange
        self._connect()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._disconnect()
        
    def _connect(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.exchange, exchange_type='fanout', durable=True)

    def _disconnect(self):
        if self.channel.is_open:
            self.channel.close()
        if self.connection.is_open:
            self.connection.close()

    def publish(self, routing_key, body, retry=2):
        properties = pika.BasicProperties(
            delivery_mode=2,
            timestamp=int(time.time() * 1000),
            content_type='b'
        )
        for i in range(retry + 1):
            try:
                return self.channel.basic_publish(
                    properties=properties,
                    exchange=EXCHANGE,
                    routing_key=routing_key,
                    body=body)
            except pika.exceptions.ConnectionClosed:
                self._connect()
            except Exception as ex:
                if self.channel.is_open:
                    self.channel.close()
                if self.connection.is_open:
                    self.channel.close()
                self._connect()
            time.sleep(1)

    def close(self):
        self._disconnect()

    def subscribe(self, routing_key, callback):
        self.callback = callback
        self.queue = self.channel.queue_declare(
            exclusive=True,
            arguments={'x-max-length': 100}
        ).method.queue

        self.channel.queue_bind(
            exchange=EXCHANGE,
            queue=self.queue,
            routing_key=routing_key
        )
        self.channel.basic_consume(
            self.callback,
            queue=self.queue,
            no_ack=True
        )


class RmqPublisher(object):
    def __init__(self, host=HOST, exchange=EXCHANGE):
        self.publisher = RmqInterface(host, exchange)

    def send(self, who, message):
        self.publisher.publish(who, message)


class RmqSubscriber(Thread):
    def __init__(self, host=HOST, exchange=EXCHANGE):
        self.host = host
        self.exchange = exchange

    def _callback(self, channel, method, properties, body):
        print(body)

    def run(self):
        try:
            with RmqInterface(self.host, self.exchange) as rmq:
        self.channel.start_consuming()

