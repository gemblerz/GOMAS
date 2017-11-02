#! /usr/bin/env python3

import zmq
import time

class Communicator(object):
    def __init__(self, id):
        self.context = zmq.Context.instance()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        self.subscriber.bind('tcp://127.0.0.1:%d' % (id,))

        #time.sleep(1)

        self.publisher = self.context.socket(zmq.PUB)
        self.list_my_consumer=[]

    def read(self):
        message = ''
        try:
            #self.subscriber.recv(zmq.DONTWAIT)
            message = self.subscriber.recv_string(flags=zmq.NOBLOCK)
            #print("msg: %s"%message)
        except zmq.error.Again:
            pass
            #print("msg doesn't come")
        return message

    def send(self, addr, message):
        #context=zmq.Context()
        #self.publisher=self.context.socket(zmq.PUB)
        if not addr in self.list_my_consumer:
            self.publisher.connect('tcp://127.0.0.1:%d' % (addr,))
            self.list_my_consumer.append(addr)

        time.sleep(1)
        #sender.send(b'')
        self.publisher.send_string(message)
        #self.publisher.disconnect('tcp://127.0.0.1:%d' % (addr,))

        #self.publisher.close()
        #self.publisher.disconnect('ipc:///tmp/%s-listener' % (addr,))
        #time.sleep(0.1)
        #sender.close()

    def close(self):
        self.publisher.close()
        self.subscriber.close()
        self.context.term()