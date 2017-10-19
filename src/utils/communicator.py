#! /usr/bin/env python3

import zmq
import threading

class Communicator(object):
    def __init__(self, id):
        self.context = zmq.Context()

        self.listener = self.context.socket(zmq.PUB)
        # self.listener.setsockopt(zmq.SUBSCRIBE, b'')
        self.listener.bind('tcp://127.0.0.1:%d' % (id,))

    def read(self):
        message = ''
        try:
            #message = self.listener.recv_string()#(flags=zmq.NOBLOCK)
            self.listener.send_string('hello world')
        except zmq.error.Again:
            pass
        return message

    def send(self, addr, message):
        socket = self.context.socket(zmq.SUB)
        socket.setsockopt(zmq.SUBSCRIBE, b'')
        socket.connect('tcp://127.0.0.1:%d' % (addr,))
        #socket.send_string(message)
        print(socket.recv_string())
        socket.close()

    def end(self):
        self.listener.close()

    def receive(self):
        while self.listener_alive:
            message = self.listener.recv()
            self.callback(message)
