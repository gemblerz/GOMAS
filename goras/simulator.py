import websocket

from agent import GorasAgent
from utils.rmq import RmqPublisher, RmqSubscriber
from s2clientprotocol import sc2api_pb2 as sc_pb

class Sc2Agent(GorasAgent):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.mouth = RmqPublisher.default()
        self.ear = RmqSubscriber.default(what_to_subscribe='sim')
        self.is_connected = False

    def _open(self, address='127.0.0.1', port=5000):
        try:
            self.conn = websocket.create_connection("ws://%s:%s/sc2api" % (address, port), timeout=60)
            self.is_connected = self.conn
            self.mouth.say('log', 'StarCraft2 is connected')
        except Exception as ex:
            self.mouth.say('log', 'Failed to launch StarCraft2')

    def _close(self):
        if self.is_connected:
            self.conn.close()

    def _interact(self):
        request = sc_pb.Request(**kwargs)
        request_str = request.SerializeToString()
        if self.is_connected:
            self.conn.send(request_str)
            response_str = self.conn.recv()
            response = sc_pb.Response()
            response.ParseFromString(response_str)
            return self.read()

    def run(self):
        while not self.time_to_exit.is_set():
            message = self.ear.hear()
            if message is not None:
                response = self._interact(message)
                self.mouth.say(to_agent, response_message)
