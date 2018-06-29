import time
import websocket
import subprocess
import os

from agent import GorasAgent
from utils.rmq import RmqPublisher, RmqSubscriber
from resources.maps import goras_maps
from s2clientprotocol import sc2api_pb2 as sc_pb
import utils.goras_message_pb2 as msg_pb


# Interpretation functions
def req_create_game():
    map_info = sc_pb.LocalMap()
    the_map = [x for x in goras_maps if 'GorasMap.SC2Map' in x]
    map_info.map_path = the_map[0]
    create_game = sc_pb.RequestCreateGame(local_map=map_info)
    create_game.player_setup.add(type=1)
    create_game.realtime = True
    return sc_pb.Request(create_game=create_game)

def res_create_game(sc_message):
    response = sc_pb.Response()
    response.ParseFromString(sc_message)
    return response

def req_join_game():
    interface_options = sc_pb.InterfaceOptions(raw=True, score=True)
    join_game = sc_pb.RequestJoinGame(race=3, options=interface_options)
    return sc_pb.Request(join_game=join_game)

def res_join_game(sc_message):
    response = sc_pb.Response()
    response.ParseFromString(sc_message)
    return response

def req_status_game():
    observation = sc_pb.RequestObservation()
    return sc_pb.Request(observation=observation)

def res_status_game(sc_message):
    response = sc_pb.Response()
    response.ParseFromString(sc_message)
    player = response.observation.player_common
    units = response.observation.raw_data.units
    return player, units

sc_actions = {
    'create_game': (req_create_game, res_create_game),
    'join_game': (req_join_game, res_join_game),
    'status_game': (req_status_game, res_status_game),
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
            self.say('log', self.create_inform(subject='simulator', verb='starts'))
            return True
        except Exception as ex:
            self.say('log', self.create_inform(subject='simulator', verb='not connect', object='StarCraft2'))
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

    def _interact(self, request):
        request_str = request.SerializeToString()
        if self.is_connected:
            self.conn.send(request_str)
            response_str = self.conn.recv()
            response = sc_pb.Response()
            response.ParseFromString(response_str)
            return response

    def _publish_env(self, player):
        self.say('resources.mineral', self.create_inform(subject='mineral', verb='is', object=str(player.minerals)))
        self.say('resources.vespene', self.create_inform(subject='vespene', verb='is', object=str(player.vespene)))
        self.say('resources.food_cap', self.create_inform(subject='food_cap', verb='is', object=str(player.food_cap)))
        self.say('resources.food_used', self.create_inform(subject='food_used', verb='is', object=str(player.food_used)))

    def _publish_units(self, units):
        for unit in units:
            tag = str(unit.tag)
            position = unit.pos
            # print(tag)
            self.say('units.' + tag + '.pos.x', self.create_inform(subject='x', verb='is', object=str(unit.pos.x)))
            self.say('units.' + tag + '.pos.y', self.create_inform(subject='y', verb='is', object=str(unit.pos.y)))

            # print(unit)
            # print(unit.unit_type, unit.is_selected)


    def run(self):
        # Launch and connect
        self._launch_simulator()
        for i in range(5):
            if self._open() is False:
                self.say('log', self.create_inform(subject='simulator', verb='retries'))
                time.sleep(5)
            else:
                break

        while not self.time_to_exit.is_set():
            sentence = self.hear()
            if sentence is not None:
                if sentence.HasField('command'):
                    command = sentence.command.action
                    if 'start_game' in command:
                        func_req, func_res = sc_actions['create_game']
                        sc_command = func_req()
                        response = self._interact(sc_command)

                        func_req, func_res = sc_actions['join_game']
                        sc_command = func_req()
                        response = self._interact(sc_command)
                        break
            time.sleep(1)

        status_update_period = 2  # in second
        last_updated = time.time()
        while not self.time_to_exit.is_set():
            # Process all requests first
            while True:
                sentence = self.hear()
                if sentence is None:
                    break
                if sentence.HasField('command'):
                    command = sentence.command.action
                    if command in sc_actions:
                        func_req, func_res = sc_actions[command]
                        sc_command = func_req()
                        response = self._interact(sc_command)
                        print(response)
                        # self.say(
                        #     who=sentence.speaker,
                        #     message=response)
            
            # Update status
            current_time = time.time()
            if (current_time - last_updated) > status_update_period:
                func_req, func_res = sc_actions['status_game']
                sc_command = func_req()
                response = self._interact(sc_command)
                if response.observation.observation.HasField('player_common'):
                    player = response.observation.observation.player_common
                    self._publish_env(player)
                if response.observation.observation.HasField('raw_data'):
                    units = response.observation.observation.raw_data.units
                    my_units = [unit for unit in units if unit.owner == 1]
                    self._publish_units(my_units)
                last_updated = current_time
            time.sleep(0.1)
