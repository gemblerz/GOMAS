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

from action import Action, get_basic_actions
from knowledge_base import Knowledge
from goal import Goal, create_goal_set

FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class Agent(object):
    def __init__(self):
        self.discrete_time_step = 1 # sec
        self.alive = False

        self.actions = get_basic_actions()
        self.knowledge = []
        self.goals = []

    def _load_knowledge(self, knowledge):
        for k in knowledge:
            self.knowledge.append(Knowledge(k))

    def _load_goals(self, goals):
        self.goals = goals

    def spawn(self, unit_id, initial_knowledge=[], initial_goals=[]):
        assert unit_id in units

        # Load basic characteristics of the unit
        self.load_unit(units[unit_id])

        # Set initial statements in knowledge
        self._load_knowledge(initial_knowledge)

        # Store initial goals
        self._load_goals(initial_goals)

        # Initialize communications
        self.init_comm_env()
        self.init_comm_agents()

        # Give it a life
        self.alive = True

    def load_unit(self, spec):
        self.id = spec['id']
        self.name = spec['name']

        for action in spec['actions']:
            assert 'id' in action
            assert 'name' in action
            assert 'require' in action

            self.actions.append(
                Action(
                    action_name=action['name'],
                    actual_code='',
                    require=action['require'],
                    sc_action_id=action['id']))

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
        logger.info('%s is performing %s' % (self.name, action))
        action.perform()
        return True

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
        Returns an action that can perform the task
    '''
    def _has_action_for_task(self, task):
        for action in self.actions:
            if action.can_perform(task.__name__):
                action.set_arguments(task.arguments)
                return action
        return None

    '''
        Returns available actions based on the desires in the current situation
    '''
    def next_action(self, current_goal, current_knowledge):
        list_actions = []
        if len(current_goal) == 0:
            # TODO: is an action always triggered by a goal?
            return None, None

        # TODO: all the goals may need to be examined
        g = current_goal.pop()
        logger.info('current goal is %s' % (g,))

        # List up possible actions that can achieve the goal
        # If the agent knows how to attain the goal
        for task in g.get_tasks():
            action = self._has_action_for_task(task)
            if action is not None:
                list_actions.append(action)

        # Select actions from the list of actions in terms of the current situation
        return_action = list_actions[0]

        # Return the most beneficial action from the selected actions
        return return_action, g

    '''
        Main logic runs here (i.e., reasoning)
    '''
    def run(self):
        while self.alive:
            # For debugging
            logger.info('%s is ticking' % (self.name,))
            # Check if something to answer
            # query = self.check_being_asked():
            # if query:
            #     self.answer(query)

            # Perceive environment
            # self.perceive()

            # Reason next action
            selected_action, selected_goal = self.next_action(self.goals, self.knowledge)

            # Perform the action
            if selected_action is not None:
                if not self.act(selected_action):
                    # Action failed, put the goal back to the queue
                    self.goals.append(selected_goal)

            # May need to tell others the action that is about to be performed
            # self.tell('%d performs %s' % (self.id, action))
            # Or
            # May tell others the action has performed

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
    probe.spawn(84,
        initial_knowledge=[
            ('type1', 'my_name', ['probe']),
            ('type2', 'i', 'say', ['my_name']),
            ],
        initial_goals=[
            create_goal_set({'goal': 'say hello', 'require': [['say', {'words':'hello'}]]}),
            ]
        )
    print('Agent is running...')
    try:
        probe.run()
    except KeyboardInterrupt:
        pass
    probe.destroy()
    print('The agent is terminated.')
