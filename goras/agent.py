from threading import Thread, Event

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

    def create_sentence_inform(self, **kwargs):
        inform = msg_pb.GorasInform(**kwargs)
        sentence = msg_pb.GorasSentence(inform=inform)
        return sentence.SerializeToString()

    def interpret(self, message):
        interpreted = msg_pb.GorasSentence()
        interpreted.ParseFromString(message)
        return interpreted

    def run(self):
        raise NotImplemented('run method must exist')
