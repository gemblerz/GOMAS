#! /usr/bin/env python3

import zmq
import threading
import time

class Communicator(object):
    def __init__(self, id):
        self.context = zmq.Context()
        self.listener = self.context.socket(zmq.PAIR)
        self.listener.bind('ipc:///tmp/%s-listener' % (id,))
        #self.listener.setsockopt(zmq.SUBSCRIBE, b'')

    def read(self):
        message = ''
        try:
            message = self.listener.recv_string(flags=zmq.NOBLOCK)
            print("msg: %s"%message)
        except zmq.error.Again:
            print("msg doesn't come")
        return message

    def send(self, addr, message):
        #pcontext=zmq.Context()
        sender = self.context.socket(zmq.PAIR)
        sender.connect('ipc:///tmp/%s-listener' % (addr,))
        time.sleep(0.1)
        sender.send_string(message)
        sender.close()

    def close(self):
        self.listener.close()