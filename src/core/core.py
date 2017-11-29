#!/usr/bin/python3

"""
    This is a core module that supports fundamental componets to run simulation.
"""

import logging
import threading
import argparse
import os
import time
import sys
import json
sys.path.append('../agent')
from agent import Agent
from goal import Goal, create_goal_set

from sc2_comm import sc2
from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import raw_pb2 as raw_pb

from utils.communicator import Communicator, proxy

from google.protobuf import json_format

FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

class Core(object):

    def __init__(self):
        self.comm_sc2 = sc2()
        self.port = 5000

        if sys.platform == "darwin": # Mac OS X
            self.launcher_path = "/Applications/StarCraft\ II/Support/SC2Switcher.app/Contents/MacOS/SC2Switcher\
                                  --listen 127.0.0.1\
                                  --port %s"%self.port
            self.map_path = os.getcwd()+'/../../resource/Maps/GorasMap.SC2Map'

        elif sys.platform == "win32": # Windows

            self.launcher_path = 'C:\\"Program Files (x86)"\\"StarCraft II"\\"Support"\SC2Switcher.exe --listen 127.0.0.1 --port %s"'%self.port
            self.map_path = os.getcwd()+'/../../resource/Maps/GorasMap.SC2Map'

        else:
            logger.error("Sorry, we cannot start on your OS.")

        # Communicator between the core and agents.
        self.comm_agents = Communicator(topic='core')

        # Set the Proxy and Agents Threads.
        self.thread_proxy = threading.Thread(target=proxy)
        self.threads_agents = []

        # for test two agent sys
        self.spawned_agent=0

        # Set the dictionary to save the information from SC2 client.
        # Not Used Yet
        self.dict_probe = {}
        self.dict_mineral = {}
        self.dict_nexus = {}
        self.next_pylon_pos=(27,33)

    def init(self, launch_sc2=True):

        if launch_sc2:
            #execute SC2 client.
            try:
                os.system(self.launcher_path)

                time.sleep(5) # need time to connect after launch app.

            except:
                logger.error("Failed to open sc2.")

        #connection between core and sc2_client using sc2 protobuf.
        self.comm_sc2.open()

    def deinit(self):
        self.comm_agents.close()
        self.comm_sc2.close()

    def log(self, message):
        self.comm_agents.log(message, 'core')

    '''
        Collection of Requests to SC2 client.
        
            Includes,
            - _start_new_game
                    After starting SC2 client, to start the game, we have to select the map and request to open the game.
                    Set the game configuration, and request to join that game.
            - _leave_game
                    When the goal-oriented simulation is finished, Leave the game to end program.
            - _quit_sc2
                    Quit the SC2 client program.
            - _train_probe
                    Train a probe in nexus.
                    It doesn't wait for spawning a probe, so cannot start a new agent thread.
            - _build_pylon
                    Build the pylon on storage_area which is start from (x,y) = (27,33), add 2 to x after that.
            - _req_playerdata
                    Request the basic information data to SC2 client.
                    Update some data 'dict_probe', 'dict_pylon', 'dict_nexus'.
                    Return the tuple that includes 'the amount of minerals', 'food capacity', 'food used'
    '''
    def _start_new_game(self):

        # create a game
        try:
            map_info = sc_pb.LocalMap()

            map_info.map_path = self.map_path
            create_game = sc_pb.RequestCreateGame(local_map=map_info)
            create_game.player_setup.add(type=1)
            # create_game.player_setup.add(type=2)

            create_game.realtime = True

            # send Request
            print(self.comm_sc2.send(create_game=create_game))
            # print (test_client.comm.read())

            logger.info('New game is created.')
        except Exception as ex:
            logger.error('While creating a new game: %s'%str(ex))

        # join the game
        try:
            interface_options = sc_pb.InterfaceOptions(raw=True, score=True)
            join_game = sc_pb.RequestJoinGame(race=3, options=interface_options)

            # send Request
            print(self.comm_sc2.send(join_game=join_game))

            logger.info('Success to join the game.')
        except Exception as ex:
            logger.error('While joining the game: %s'%str(ex))

        # Game Start
        try:
            #print(self.comm_sc2.send(step=sc_pb.RequestStep(count=1)))

            logger.info('Game is Started.')
            self.log('Simulation started!')
        except Exception as ex:
            logger.error('While starting a new game: %s'%str(ex))

    def _leave_game(self):
        print(self.comm_sc2.send(leave_game=sc_pb.RequestLeaveGame()))
        logger.info('Leave the Game.')

    def _quit_sc2(self):
        print(self.comm_sc2.send(quit=sc_pb.RequestQuit()))
        logger.info("Quit the SC2 client")

    def _train_probe(self, nexus_tag):

        unit_command = raw_pb.ActionRawUnitCommand(ability_id=1006)
        unit_command.unit_tags.append(nexus_tag)
        action_raw = raw_pb.ActionRaw(unit_command=unit_command)
        action = sc_pb.RequestAction()
        action.actions.add(action_raw=action_raw)
        t = self.comm_sc2.send(action=action)

    def _build_pylon(self, probe_tag):
        # build_pylon
        unit_command = raw_pb.ActionRawUnitCommand(ability_id=881)
        unit_command.unit_tags.append(probe_tag)
        unit_command.target_world_space_pos.x = 38
        unit_command.target_world_space_pos.y = 29
        action_raw = raw_pb.ActionRaw(unit_command=unit_command)
        action = sc_pb.RequestAction()
        action.actions.add(action_raw=action_raw)
        self.comm_sc2.send(action=action)

    def _req_playerdata(self):
        observation = sc_pb.RequestObservation()
        t = self.comm_sc2.send(observation=observation)

        for unit in t.observation.observation.raw_data.units:
            if unit.unit_type == 84: # Probe tag

                # Already exists
                if unit.tag in self.dict_probe:
                    self.dict_probe[unit.tag] = (unit.pos.x, unit.pos.y, unit.pos.z)
                else:
                    # new probe
                    if self.spawned_agent>=4:
                        continue

                    self.dict_probe[unit.tag] = (unit.pos.x, unit.pos.y, unit.pos.z)

                    # new thread starts -> spawn a new probe.
                    self.threads_agents.append(Agent())

                    # If the agent have to know their name
                    #send_knowledge={}
                    #send_knowledge.update(self.initial_knowledge)
                    #send_knowledge.update({''})

                    self.threads_agents[-1].spawn(unit.tag, 84,
                                        initial_knowledge = self.initial_knowledge,
                                        initial_goals = [create_goal_set(self.goal)],
                                        )

                    self.threads_agents[-1].start()
                    self.spawned_agent+=1

            if unit.unit_type == 341: # Mineral tag

                # Already exists
                if unit.tag in self.dict_mineral:
                    self.dict_mineral[unit.tag] = (unit.pos.x, unit.pos.y, unit.pos.z)
                else:
                    # new pylon
                    self.dict_mineral[unit.tag] = (unit.pos.x, unit.pos.y, unit.pos.z)

            if unit.unit_type == 59:
                # Already exists
                if unit.tag in self.dict_mineral:
                    self.dict_nexus[unit.tag] = (unit.pos.x, unit.pos.y, unit.pos.z)
                else:
                    # new nexus
                    self.dict_nexus[unit.tag] = (unit.pos.x, unit.pos.y, unit.pos.z)

        minerals = t.observation.observation.player_common.minerals
        food_cap = t.observation.observation.player_common.food_cap
        food_used = t.observation.observation.player_common.food_used
        print('Minerals: ',minerals)
        print('Population: %d/%d'%(food_used,food_cap))
        return (minerals,food_cap,food_used)


    '''
        Connection methods to broadast and receive msg.
        
            Includes,
            - _start_proxy
                    Start the proxy that is broker among the agents, also between core and agents.
            - broadcast
                    Usually use 'broadcast' to 'agents' from 'core' to send the status of player in SC2.
            - perceive_request
                    To get requests from agents, such as to move probe, to gather minerals.
            - set_goal
                    Set the goal tree to simulate. The goal is also consisted of dictionary.
            - set_init_kn
                    Set the initial knowledge base. It is needed when the agents has spawned newly.

    '''
    def _start_proxy(self):
        logger.info("Try to turn on proxy...")
        self.thread_proxy.start()
        time.sleep(1) # wait for turn on proxy

    def broadcast(self,msg):
        self.comm_agents.send(msg,broadcast=True)

    def perceive_request(self):
        return self.comm_agents.read()

    def set_goal(self):
        observation = sc_pb.RequestObservation()
        t = self.comm_sc2.send(observation=observation)

        list_minerals=[]

        for unit in t.observation.observation.raw_data.units:
            if unit.unit_type == 341:  # Mineral tag
                list_minerals.append(unit.tag)



        self.goal = {'goal': 'gather 50 minerals',
                     'trigger': [],
                     'satisfy': [
                         ('type2', 'i', 'have', ['100 minerals'])
                     ],
                     'precedent': [],
                     'require': [
                         ['gather 1', {'target': 'unit', 'unit_tag': list_minerals[0]}, 'General'],  # target: unit
                         ['gather 2', {'target': 'unit', 'unit_tag': list_minerals[0]}, 'General'],
                         ['gather 3', {'target': 'unit', 'unit_tag': list_minerals[0]}, 'General'],
                         ['gather 4', {'target': 'unit', 'unit_tag': list_minerals[0]}, 'General'],
                         ['check mineral 1', {'target': 'minerals', 'amount': 50}, 'Query'],
                         #['check mineral 2', {'target': 'minerals', 'amount': 20}, 'Query'],
                     ]

                     }

    def set_init_kn(self):
        self.initial_knowledge =    { self.goal['goal'] : { 'is' : 'Not Assigned' },
                                      'gather 1' : { 'is' : 'Ready' },
                                      'gather 2' : { 'is' : 'Ready' },
                                      'gather 3' : { 'is' : 'Ready' },
                                      'gather 4' : { 'is' : 'Ready' },
                                      'check mineral 1' : { 'is' : 'Ready'},
                                      #'check mineral 2' : { 'is' : 'Ready'}
                                    }

    '''
        The Main Part of Core.
    '''
    def run(self):

        self._start_new_game()
        self._start_proxy()
        self.set_goal()
        self.set_init_kn()

        while True:

            logger.info('%s is ticking' % ('core'))

            minerals,food_cap,food_used=self._req_playerdata()

            # Tell game data to everyone.
            data = {}
            data['minerals']={}
            data['minerals']['gathered'] = str(minerals)
            #data['minerals']['are']=list(self.dict_mineral.items())
            #data['food']={}
            #data['food']['has'] = str(food_cap)
            #data['food']['used'] = str(food_used)
            #data['probes']={'are':self.dict_probe.items()}
            #data['nexus']={'are':self.dict_nexus.items()}

            json_string=json.dumps(data)
            self.broadcast(json_string)

            # Check the End condition
            probes_status=False
            for probe in self.threads_agents:
                if probe.isAlive(): # Remain the alive probe. Core must run.
                    probes_status=True
                    break

            # No alive Agents. Exit the program.
            if probes_status is False:
                self._leave_game()
                self._quit_sc2()
                break


            # Get Requests from agents.
            for i in range(len(self.threads_agents)):
                req=self.perceive_request()
                if req.startswith('core'):
                    req=req[5:]
                    req=json_format.Parse(req,sc_pb.RequestAction())
                    #json.loads(req)
                    self.comm_sc2.send(action=req)

            #TODO : Randomly Occured Error...
            #self._train_probe(list(self.dict_nexus.keys())[0])

            time.sleep(0.5)

        print("Test Complete")
        self.comm_agents.context.term()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--launch', action='store_true', help='Launch sc2 instance')

    args = parser.parse_args()

    core = Core()
    logger.info('Core initializing...')
    core.init(launch_sc2=args.launch)
    logger.info('Core running...')
    core.run()
    logger.info('Core deinitializing...')
    core.deinit()
    logger.info('Core terminated.')