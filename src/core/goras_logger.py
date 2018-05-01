import sys

sys.path.append('../')

from utils.rmq import RmqSubscriber
from threading import Thread, Event

class GorasAgent(Thread):
    def __init__(self):
        super().__init__()
        self.time_to_exit = Event()
        self.time_to_exit.clear()

    def terminate(self):
        self.time_to_exit.set()
        self.join()

    def run(self):
        raise NotImplemented('run method must exist')


class GorasLogger(GorasAgent):
    def __init__(self):
        super().__init__()
        self.history_path = '/tmp/simulation.history'
        self.ear = RmqSubscriber.default(what_to_hear='*')

    def terminate(self):
        super().terminate()
        self.ear.close()

    def run(self):
        with open(self.history_path, 'w') as log:
            while not self.time_to_exit.is_set():
                message = self.ear.read()
                if message is not None:
                    timestamp, body = message
                    tiemstamp /= 1000
                    formatted = '{},{}'.format(timestamp, body)
                    log.write()
                time.sleep(0.1)
