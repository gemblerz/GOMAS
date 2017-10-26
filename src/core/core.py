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

from units import units

from sc2_comm import sc2
from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import raw_pb2 as raw_pb

FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

class Core(object):

    def __init__(self):
        self.comm = sc2()
        self.port = 5000

        if sys.platform == "darwin": # Mac OS X
            self.launcher_path = "/Applications/StarCraft\ II/Support/SC2Switcher.app/Contents/MacOS/SC2Switcher\
                                  --listen 127.0.0.1\
                                  --port %s"%self.port
            self.map_path = os.getcwd()+'/../../resource/Maps/GorasMap.SC2Map'

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

    def _start_new_game(self):

        # create a game
        try:
            map_info = sc_pb.LocalMap()

            map_info.map_path = self.map_path
            create_game = sc_pb.RequestCreateGame(local_map=map_info)
            create_game.player_setup.add(type=1)
            create_game.player_setup.add(type=2)

            create_game.realtime = True

            # send Request
            print(self.comm.send(create_game=create_game))
            # print (test_client.comm.read())

            logger.info('New game is created.')
        except Exception as ex:
            logger.error('While creating a new game: %s'%str(ex))

        # join the game
        try:
            interface_options = sc_pb.InterfaceOptions(raw=True, score=True)
            join_game = sc_pb.RequestJoinGame(race=3, options=interface_options)

            # send Request
            print(self.comm.send(join_game=join_game))

            logger.info('Success to join the game.')
        except Exception as ex:
            logger.error('While joining the game: %s'%str(ex))

        # Game Start
        try:
            print(self.comm.send(step=sc_pb.RequestStep(count=1)))

            logger.info('Game is Started.')
        except Exception as ex:
            logger.error('While starting a new game: %s'%str(ex))


    def run(self):

        self._start_new_game()

        list_unit_tag = []
        observation = sc_pb.RequestObservation()
        t = self.comm.send(observation=observation)

        for unit in t.observation.observation.raw_data.units:
            if unit.unit_type == 84:  # Probe unit_type_tag
                list_unit_tag.append(unit.tag)

        action=raw_pb.ActionRawUnitCommand(ability_id=4)
        action.unit_tags.append(list_unit_tag[0])
        action_raw = raw_pb.ActionRaw(unit_command=action)

        action = sc_pb.RequestAction()
        action.actions.add(action_raw=action_raw)
        self.comm.send(action=action)

        probe = Agent()
        probe.spawn(list_unit_tag[0], 84,
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