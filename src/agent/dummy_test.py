#!/usr/bin/python3

import sys
import threading
import time
import random
import logging
from datetime import datetime
from agent import Agent

sys.path.append('../')
from utils.communicator import Communicator, proxy
from goal import Goal, create_goal_set

FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

class AgentThread(threading.Thread):
    def __init__(self, name, counter, unit_id, initial_knowledge=[], initial_goals=[], core=False):
        logging.info(name+' Thread starts initializing...')

        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.who = Agent()
        self.who.spawn(counter, unit_id, initial_knowledge, initial_goals)
        #self.set_arguments(counter, unit_id, initial_knowledge, initial_goals)
        self.who.init_comm_agents(core)
        logging.info(self.name+' is Initialzied')

    def run(self):
        print('Agent is running...')
        try:
            self.who.run()
        except KeyboardInterrupt:
            pass
        #self.who.destroy()
        print('The agent %s is terminated.'%(self.name))

    """
    def set_arguments(self, spawn_id, unit_id, initial_knowledge=[], initial_goals = []):
        self.who.spawn(spawn_id, unit_id, initial_knowledge, initial_goals)
    """



if __name__ == '__main__':

    proxy_thread = threading.Thread(target=proxy)

    goal = {'goal': 'gather_100_minerals',
            'trigger': [],
            'satisfy': [
                ('type2', 'i', 'have', ['100 minerals'])
            ],
            'precedent': [],
            'require': [
                ['move', {'target': 'point', 'pos_x': 10, 'pos_y': 10}],
                ['gather', {'target': 'unit', 'unit_tag': 'list_mineral_tag[0]'}],
            ]
            }

    agent_knowledge = [
        ('type1', 'my_name', ['agent']),
        ('type1', 'my_state', ['Idle']),
    ]

    dummy_knowledge = [
        ('type1', 'my_name', ['dummy']),
        ('type1', 'my_state', ['Idle']),
    ]



    threads=[]
    agent = AgentThread("Henry", 1, 84, initial_knowledge=agent_knowledge, initial_goals=[create_goal_set(goal)])
    dummy = AgentThread("Dummy", 2, 84, initial_knowledge=dummy_knowledge, initial_goals=[create_goal_set(goal)])
    threads.append(agent)
    threads.append(dummy)

    time.sleep(1)

    proxy_thread.start()

    time.sleep(1)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()






