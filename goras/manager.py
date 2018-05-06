#! /usr/bin/python3

import os
import subprocess
import time
import threading
from logger import GorasLogger
from simulator import Sc2Agent


def launch_backbone():
    launch_script = 'rabbitmq-server -detached'
    os.system(launch_script)


class GorasManager(object):
    def __init__(self):
        self.agents = []
        self.simulator = None
        self.logger = None

    def __enter__(self):
        return self

    def __exit__(self ,type, value, traceback):
        for agent in self.agents:
            agent.terminate()
            agent.join(timeout=5.)
        if self.simulator is not None:
            self.simulator.terminate()
            self.simulator.join()
        if self.logger is not None:
            self.logger.terminate()
            self.logger.join()
        return

    def configure(self):
        # Launch backbone network
        launch_backbone()

        # Spawn logger
        self.logger = GorasLogger()
        self.logger.start()

        # Start simulator
        self.simulator = Sc2Agent()
        self.simulator.start()

    def check_before_go(self):
        pass

    def run(self):
        input('Press Enter when ready')

        # query = msg_pb.GorasCommand(action='create_game')
        # sentence = msg_pb.GorasSentence(id=count, speaker='testagent', command=query)
        # print(sentence)
        # self.mouth.say('sim', sentence.SerializeToString())

        # interface_options = sc_pb.InterfaceOptions(raw=True, score=True)
        # join_game = sc_pb.RequestJoinGame(race=3, options=interface_options)

        # # send Request
        # print(self.comm_sc2.send(join_game=join_game))
