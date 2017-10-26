#!/usr/bin/python3

"""
    This is a core module that supports fundamental componets to run simulation.
"""

import logging
import zmq
import os
import time

import sys
sys.path.append('../agent')
from agent import Agent
from goal import Goal, create_goal_set

from sc2_comm import sc2
from s2clientprotocol import sc2api_pb2 as sc_pb

FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

class Core(object):

    def __init__(self):
        self.comm = sc2()
        self.port = 5000

        if sys.platform == "darwin": # Mac OS X
            self.launcher_path = "/Applications/StarCraft\ II/Support/SC2Switcher.app/Contents/MacOS/SC2Switcher --listen 127.0.0.1 --port %s"%self.port
            self.map_path = "/Applications/StarCraft II/Maps/mini_games/GorasMap.SC2Map"

        elif sys.platform == "win32": # Windows
            pass
            #self.launcher_path =
            #self.map_path =

        else:
            logger.error("Sorry, we cannot start on your OS.")

    def init(self):

        # execute SC2 client.
        try:
            os.system(self.launcher_path)

            time.sleep(5) # need time to connect after launch app.

        except:
            logger.error("Failed to open sc2.")

        #connection between core and sc2_client using sc2 protobuf.
        self.comm.open()

    def deinit(self):
        pass

    def _create_new_game(self):
        # create a game

        map_info = sc_pb.LocalMap()
        # Windows
        # map_info.map_path = "C:\Program Files (x86)\StarCraft II\Maps\Melee\Simple128.SC2Map"
        # Mac
        map_info.map_path = self.map_path
        create_game = sc_pb.RequestCreateGame(local_map=map_info)
        create_game.player_setup.add(type=1)
        create_game.player_setup.add(type=2)

        create_game.realtime = True
        # print("Make")
        # send Request
        print(self.comm.send(create_game=create_game))
        # print (test_client.comm.read())

        logger.info('Game created.')

    def run(self):

        self._create_new_game()
        """Join Game"""
        # Make Requst(JoinGame)

        interface_options = sc_pb.InterfaceOptions(raw=True, score=True)
        join_game = sc_pb.RequestJoinGame(race=3, options=interface_options)

        # send Request
        self.comm.send(join_game=join_game)
        # print (test_client.comm.read())

        # Game Start
        self.comm.send(step=sc_pb.RequestStep(count=1))
        # print (test_client.comm.read())

        logger.info('Game Started.')


        unit_tag_list = []
        observation = sc_pb.RequestObservation()
        t = self.comm.send(observation=observation)

        for unit in t.observation.observation.raw_data.units:
            if unit.unit_type == 84:  # Probe unit_type_tag
                unit_tag_list.append(unit.tag)

        probe = Agent()
        probe.spawn(unit_tag_list[0], 84,
                    initial_knowledge=[
                        ('type1', 'my_name', ['probe']),
                        ('type2', 'i', 'say', ['my_name']),
                    ],
                    initial_goals=[
                        create_goal_set(
                            {'goal': 'introduce myself',
                             'require':
                                 [['say', {'words': 'hello'}],
                                  {'goal': 'say hello',
                                   'require':
                                       [['say', {'words': 'myname'}]]}
                                  ]
                             }),
                    ]
                    )
        print('Agent is running...')
        try:
            probe.run()
        except KeyboardInterrupt:
            pass
        probe.destroy()
        print('The agent is terminated.')







if __name__ == '__main__':
    core = Core()
    logger.info('Core initializing...')
    core.init()
    logger.info('Core running...')
    core.run()
    logger.info('Core deinitializing...')
    core.deinit()
    logger.info('Core terminated.')