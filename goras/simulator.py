import websocket
import subprocess
import os

from agent import GorasAgent
from utils.rmq import RmqPublisher, RmqSubscriber
from resources.maps import goras_maps
from s2clientprotocol import sc2api_pb2 as sc_pb
import utils.goras_message_pb2 as msg_pb


# Interpretation functions
def create_game():
    map_info = sc_pb.LocalMap()
    map_info.map_path = goras_maps[0]
    create_game = sc_pb.RequestCreateGame(local_map=map_info)
    create_game.player_setup.add(type=1)
    create_game.realtime = True
    return {'create_game': create_game}

sc_actions = {
    'create_game': create_game,
}


class Sc2Agent(GorasAgent):
    def __init__(self):
        super().__init__(what_to_hear='sim')
        self.conn = None
        self.is_connected = False
        self.pid = None
        self.address = '127.0.0.1'
        self.port = 5000
        self.simulator_path='/Applications/StarCraft\ II/Support/SC2Switcher.app/Contents/MacOS/SC2Switcher --listen %s --port %s' % (self.address, self.port)

    def _open(self):
        try:
            self.conn = websocket.create_connection("ws://%s:%s/sc2api" % (self.address, self.port), timeout=60)
            self.is_connected = self.conn
            self.mouth.say('log', self.create_sentence_inform(content='StarCraft2 is connected'))
            return True
        except Exception as ex:
            self.mouth.say('log', self.create_sentence_inform(content='Failed to connect StarCraft2'))
            return False

    def terminate(self):
        super().terminate()
        if self.is_connected:
            self.conn.close()

    def _get_sc2_pid(self):
        p = subprocess.Popen(['pgrep', 'SC2'], stdout=subprocess.PIPE)
        pid = p.communicate()[0].strip().decode()
        try:
            return int(pid)
        except Exception:
            return -1

    def _launch_simulator(self):
        self.pid = self._get_sc2_pid()
        if self.pid < 0:
            error_code = os.system(self.simulator_path)
            if error_code == 0:
                self.pid = self._get_sc2_pid()

    def _interact(self, **kwargs):
        request = sc_pb.Request(**kwargs)
        request_str = request.SerializeToString()
        if self.is_connected:
            self.conn.send(request_str)
            response_str = self.conn.recv()
            response = sc_pb.Response()
            response.ParseFromString(response_str)
            return self.read()

    def run(self):
        self._launch_simulator()
        self._open()

        while not self.time_to_exit.is_set():
            message = self.ears.hear()
            if message is not None:
                sentence = self.interpret(message)
                if sentence.HasField('command'):
                    command = sentence.command.action
                    if command in sc_actions:
                        function = sc_actions[command]
                        sc_command = function()
                        print(sc_command)
                        # response = self._interact(sc_command)
                #print(sentence)
                #response = self._interact(message)
                #self.mouth.say(to_agent, response_message)
