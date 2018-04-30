#! /usr/bin/python3

import time
import threading

class GorasManager(object):
    def __init__(self, launcher):
        self.launcher = launcher
        self.agents = None
        self.simulator = None
        self.logger = None

    def _configure_logger(self):
        self.logger = 

    def check_before_go(self):
        if self.