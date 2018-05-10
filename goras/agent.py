from threading import Thread, Event
from time import time

from utils.rmq import RmqSubscriber, RmqPublisher
import utils.goras_message_pb2 as msg_pb


class GorasAgent(Thread):
    def __init__(self, need_ears=True, what_to_hear='*', need_mouth=True):
        super().__init__()
        self.time_to_exit = Event()
        self.time_to_exit.clear()
        self.ears = None
        self.mouth = None
        if need_ears:
            self.ears = RmqSubscriber.default(what_to_hear=what_to_hear)
        if need_mouth:
            self.mouth = RmqPublisher.default()

    def terminate(self):
        self.time_to_exit.set()
        if self.ears is not None:
            self.ears.close()
        if self.mouth is not None:
            self.mouth.close()
        self.join()

    def create_inform(self, **kwargs):
        return msg_pb.GorasInform(**kwargs)

    def listen(self, topic):
        if self.ears is None:
            return None
        

    def hear(self):
        if self.ears is None:
            return None
        message = self.ears.hear()
        if message is not None:
            interpreted = msg_pb.GorasSentence()
            interpreted.ParseFromString(message)
            return interpreted
        else:
            return None

    def say(self, who, message):
        if self.mouth is None:
            return None
        if isinstance(message, msg_pb.GorasInform):
            sentence = msg_pb.GorasSentence(when=time(), inform=message)
        elif isinstance(message, msg_pb.GorasCommand):
            sentence = msg_pb.GorasSentence(when=time(), command=message)
        if sentence is not None:
            self.mouth.say(who, sentence.SerializeToString())

    def run(self):
        raise NotImplemented('run method must exist')
