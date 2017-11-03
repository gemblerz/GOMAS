#! /usr/bin/env python3

import zmq
import time

proxy_addr_in = 'tcp://127.0.0.1:5555'
proxy_addr_out = 'tcp://127.0.0.1:5556'

class Communicator(object):
    def __init__(self, id):
        self.context = zmq.Context.instance()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        self.subscriber.connect(proxy_addr_out)
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.connect(proxy_addr_in)

        time.sleep(1)

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

    def send(self, addrs, message):

        self.publisher.send_string(message)

    def close(self):
        self.publisher.close()
        self.subscriber.close()
        self.context.term()

def proxy():
    addr_in = proxy_addr_in
    addr_out = proxy_addr_out

    context = zmq.Context.instance()
    socket_in = context.socket(zmq.XSUB)
    socket_in.bind(addr_in)
    socket_out = context.socket(zmq.XPUB)
    socket_out.bind(addr_out)

    try:
        zmq.proxy(socket_in, socket_out)
    except zmq.ContextTerminated:
        print("proxy terminated")
        socket_in.close()
        socket_out.close()
