#!/usr/bin/python3

"""
    Class Agent
    This contains core components,
        - knowledge: manages statements (e.g., I am at (x, y))
        - action: lists possible actions
        - goal: explains details of goals
        - reasoning: the brain
        - comm: ability to communicate with others
"""
import sys
import time
import logging
sys.path.append('../')
from units import units

from action import Action
from knowledge_base import Knowledge
from goal import Goal

FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class Agent(object):
    def __init__(self):
        self.discrete_time_step = 1 # sec
        self.alive = False

    def spawn(self, unit_id, initial_knowledge={}, initial_goals={}):
        assert unit_id in units

        # Load basic characteristics of the unit
        self.load_unit(units[unit_id])

        # Set initial statements in knowledge
        self.knowledge = Knowledge(initial_knowledge)

        # Store initial goals
        self.goals = Goal(initial_goals)

        # Initialize communications
        self.init_comm_env()
        self.init_comm_agents()

        # Give it a life
        self.alive = True

    def load_unit(self, spec):
        self.id = spec['id']
        self.name = spec['name']

        self.actions = Action(spec['actions'])

    '''
        Communication to simulator
    '''
    def init_comm_env(self):
        pass

    def deinit_comm_env(self):
        pass

    '''
        Communication to other agents
    '''
    def init_comm_agents(self):
        pass

    def deinit_comm_agents(self):
        # It may need to send 'good bye' to others
        pass

    '''
        Destroy myself
    '''
    def destroy(self):
        # Close communications
        self.deinit_comm_env()
        self.deinit_comm_agents()
        self.alive = False

    '''
        Information / actions going to simulator
    '''
    def act(self, action):
        pass

    '''
        Delivering information to other agents
    '''
    def tell(self, statement):
        pass

    '''
        Query to other agents
    '''
    def ask(self, query, wait_timeout=3):
        pass

    '''
        Main logic runs here (i.e., reasoning)
    '''
    def run(self):
        while self.alive:
            # Check if something to answer
            # query = self.check_being_asked():
            # if query:
            #     self.answer(query)

            # Perceive environment
            # self.perceive()

            # Reason next action
            action = self.actions.next_action(self.goal, self.knowledge.list())

            # Perform the action
            self.act(action)

            # May need to tell others the action that is about to be performed
            # self.tell('%d performs %s' % (self.id, action))

            # Sleep a while to prevent meaningless burst looping
            time.sleep(self.discrete_time_step)

        # Stopped thinking
        # Means it is dead
        # bye bye

'''
    For testing
'''
if __name__ == '__main__':
    probe = Agent()
    probe.spawn(84, [('apple', 'red')])
    try:
        probe.run()
    except KeyboardInterrupt:
        pass
    probe.destroy()