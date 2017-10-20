import zmq
import threading
import time

class Communicator(object):
    def __init__(self, id):
        self.context = zmq.Context()
        self.ssocket = self.context.socket(zmq.SUB)
        self.ssocket.setsockopt(zmq.SUBSCRIBE, b'')
        self.ssocket.bind('tcp://127.0.0.1:%d' % (id,))

    def send(self):
        message = ''
        try:
            #message = self.listener.recv_string()#(flags=zmq.NOBLOCK)
            self.psocket.send_string('hello world')
        except zmq.error.Again:
            pass
        return message

    def connect(self, addr):
        self.psocket = self.context.socket(zmq.PUB)
        self.psocket.connect('tcp://127.0.0.1:%d' % (addr,))
        for i in range(1):
            time.sleep(0.5)
            try:
                self.ssocket.recv(zmq.NOBLOCK)
            except:
                pass

    def end(self):
        self.ssocket.close()

    def receive(self):
        message = self.ssocket.recv()
        print(message)

