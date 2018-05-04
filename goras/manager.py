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
        pass