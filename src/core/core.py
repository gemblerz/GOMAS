#!/usr/bin/python3

"""
    This is a core module that supports fundamental componets to run simulation.
"""

import logging
import zmq

from sc2_comm import sc2


FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

class Core(object):
    def __init__(self):
        self.comm = sc2()

    def init(self):
        self.comm.open()

    def deinit(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    core = Core()
    logger.info('Core initializing...')
    core.init()
    logger.info('Core running...')
    core.run()
    logger.info('Core deinitializing...')
    core.deinit()
    logger.info('Core terminated.')