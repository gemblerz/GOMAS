#! /usr/bin/env python3

import zmq
import time

class Communicator(object):
    def __init__(self, id):
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.bind('ipc:///tmp/%s-listener' % (id,))
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, '')

        #time.sleep(1)

        self.publisher = self.context.socket(zmq.PUB)

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
        self.publisher.connect('ipc:///tmp/%s-listener' % (addr,))

        time.sleep(0.1)
        #sender.send(b'')
        self.publisher.send_string(message,flags=zmq.NOBLOCK)
        #self.publisher.close()
        #sender.close()

    def close(self):
        self.publisher.close()
        self.subscriber.close()