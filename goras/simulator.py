import websocket

from agent import GorasAgent
from utils.rmq import RmqPublisher, RmqSubscriber
from s2clientprotocol import sc2api_pb2 as sc_pb
import utils.goras_message_pb2 as msg_pb


# Interpretation functions
def create_game(map_path):
    map_info = sc_pb.LocalMap()
    map_info.map_path = map_path
    create_game = sc_pb.RequestCreateGame(local_map=map_info)
    create_game.player_setup.add(type=1)
    create_game.realtime = True
    return create_game

dict_words = {
    'create_game': create_game,
}


class Sc2Agent(GorasAgent):
    def __init__(self):
        super().__init__(what_to_hear='sim')
        self.conn = None
        self.is_connected = False

    def _open(self, address='127.0.0.1', port=5000):
        try:
            self.conn = websocket.create_connection("ws://%s:%s/sc2api" % (address, port), timeout=60)
            self.is_connected = self.conn
            self.mouth.say('log', 'StarCraft2 is connected')
            return True
        except Exception as ex:
            self.mouth.say('log', 'Failed to launch StarCraft2')
            return False

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
        #self._open()

        while not self.time_to_exit.is_set():
            message = self.ears.hear()
            if message is not None:
                sentence = self.interpret(message)
                print(sentence)
                #response = self._interact(message)
                #self.mouth.say(to_agent, response_message)

s = Sc2Agent()
try:
    s.run()
except:
    pass
s._close()