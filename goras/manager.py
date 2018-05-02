#! /usr/bin/python3

import time
import threading
from goras_logger import GorasLogger

class GorasManager(object):
    def __init__(self, launcher):
        self.launcher = launcher
        self.agents = None
        self.simulator = None
        self.logger = None

    def _configure_logger(self):
        self.logger = GorasLogger()

    def check_before_go(self):
        if self.