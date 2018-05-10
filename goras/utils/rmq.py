import pika
import time
from collections import deque
from threading import Thread, Event

HOST = 'amqp://localhost'
EXCHANGE = 'goras_exchange'


class _RmqInterface(object):
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
        self.channel.exchange_declare(self.exchange, exchange_type='topic', durable=True)
        self.queue = self.channel.queue_declare(
            exclusive=True,
            #arguments={'x-max-length': 256}
        ).method.queue

    def _disconnect(self):
        try:
            if self.channel.is_open:
                self.channel.close()        
            if self.connection.is_open:
                self.connection.close()
        except pika.exceptions.ConnectionClosed:
            pass

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
            except Exception:
                if self.channel.is_open:
                    self.channel.close()
                if self.connection.is_open:
                    self.channel.close()
                self._connect()
            time.sleep(1)

    def close(self):
        self._disconnect()

    def begin_subscribe(self, routing_key):
        self.channel.queue_bind(
            exchange=EXCHANGE,
            queue=self.queue,
            routing_key=routing_key
        )
        return self.queue

    def end_subscribe(self, routing_key):
        self.channel.queue_unbind(
            exchange=EXCHANGE,
            queue=self.queue,
            routing_key=routing_key
        )
        return self.queue


class RmqPublisher(object):
    def __init__(self, host=HOST, exchange=EXCHANGE):
        self.publisher = _RmqInterface(host, exchange)

    def close(self):
        self.publisher.close()

    def say(self, who, message):
        self.publisher.publish(who, message)

    @classmethod
    def default(cls):
        return cls(host=HOST, exchange=EXCHANGE)


class RmqSubscriber(Thread):
    def __init__(self, host=HOST, exchange=EXCHANGE, what_to_subscribe='*'):
        super().__init__()
        self.host = host
        self.exchange = exchange
        self.what_to_subscribe = what_to_subscribe
        self.memory = deque(maxlen=1000)
        self.time_to_exit = Event()
        self.time_to_exit.clear()
        self.start()

    @classmethod
    def default(cls, what_to_hear):
        return cls(host=HOST, exchange=EXCHANGE, what_to_subscribe=what_to_hear)

    def close(self):
        self.time_to_exit.set()
        self.join()

    def hear(self):
        try:
            return self.memory.popleft()
        except Exception:
            return None

    def run(self):
        while not self.time_to_exit.is_set():
            try:
                with _RmqInterface(self.host, self.exchange) as rmq:
                    queue = rmq.begin_subscribe(self.what_to_subscribe)
                    while not self.time_to_exit.is_set():
                        method_frame, header_frame, body = rmq.channel.basic_get(queue)
                        if method_frame:
                            self.memory.append(body)
                            rmq.channel.basic_ack(method_frame.delivery_tag)
                        else:
                            time.sleep(0.2)
            except Exception:
                pass
