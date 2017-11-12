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
import threading
import json

sys.path.append('../')
from units import units
from utils.communicator import Communicator

from action import Action, get_basic_actions
from knowledge_base import Knowledge
from goal import Goal, create_goal_set


FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

class MentalState(object):
    '''
        State machine
            Idle: Agent performs nothing, no action needed

    '''
    def __init__(self):
        self.state = 'idle'

    def change_state(self):
        self.state = 'working'

class Agent(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


        self.discrete_time_step = 1 # sec
        self.alive = False
        self.state = MentalState()

        self.actions = get_basic_actions()
        self.knowledge = {}
        self.goals = []
        self.messages = []

    def _load_knowledge(self, knowledge):
        for key,value in knowledge.items():
            self.knowledge[key]=value
            #self.tuple_to_knowledge(k)
            #self.knowledge.append(k)

    def _load_goals(self, goals):
        self.goals = goals

    def spawn( self, spawn_id, unit_id, initial_knowledge=[], initial_goals=[]):
        logging.info(str(spawn_id) + ' is being spawned...')

        assert unit_id in units

        # Identifier for the unit
        self.spawn_id = spawn_id
        print("{} is spawned".format(spawn_id))

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

        logging.info(str(spawn_id) + ' has spawned.')

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
        #self.comm_agents = Communicator(self.spawn_id)
        self.comm_agents = Communicator()

    def deinit_comm_agents(self):
        # It may need to send 'good bye' to others
        self.comm_agents.close()

    '''
        Destroy myself
        Assumption : When the agent check that the goal is achieved, destory itself.
    '''
    def destroy(self):
        # Need to broadcast "I am destroying"
        msg = "{} destroy".format(self.spawn_id)
        self.comm_agents.send(msg)
        # Close communications
        self.deinit_comm_env()
        self.deinit_comm_agents()
        self.alive = False

        self.join()

    '''
        Sense information from its surroundings and other agents
    '''
    def perceive(self):
        # Perceive from the environment (i.e., SC2)

        # Perceive from other agents
        message = self.comm_agents.read()
        if message.startswith('broadcasting'):
            message=message[13:]
            if message.startswith('{'):
                self.json_to_knowledge(message)
            else:
                self.msg_to_knowledge(message)
        self.messages.append(message)


    def json_to_knowledge(self, message):
        json_msg = json.loads(message)
        has_minerals = json_msg["has_minerals"]
        food_cap = json_msg["food_cap"]
        food_used = json_msg["food_used"]
        probe = json_msg["probe"]  #probe dictionary
        minerals = json_msg["minerals"] #mineral dictionary
        nexus = json_msg["nexus"] #nexus dictionary
        self.knowledge.append(Knowledge('type1', 'has_minerals', has_minerals))



    """
        Change msg(str) to Knowledge
    """
    def msg_to_knowledge(self, message):
        splited_msg = message.split()
        tuple_msg = tuple(splited_msg)
        if splited_msg is not None:
            if len(splited_msg) == 2:
                self.knowledge.append(Knowledge('type1', tuple_msg[0], [tuple_msg[1]]))
            elif len(splited_msg) == 3:
                self.knowledge.append(Knowledge('type2', tuple_msg[0], tuple_msg[1], [tuple_msg[2]]))
            else:
                pass
        else:
            pass

    """
        Change tuple to Knowledge
    """
    def tuple_to_knowledge(self, tuple_msg):
        if tuple_msg is not None:
            if len(tuple_msg) == 3:
                self.knowledge.append(Knowledge(tuple_msg[0], tuple_msg[1], tuple_msg[2]))
            elif len(tuple_msg) == 4:
                self.knowledge.append(Knowledge(tuple_msg[0], tuple_msg[1], tuple_msg[2], tuple_msg[3]))
            else:
                pass
        else:
            pass



    '''
        Information / actions going to simulator
    '''
    def act(self, action, task):
        self.state.change_state()

        # Update task state
        self.knowledge[task.__name__].update({'is': 'Active'})

        logger.info('%s %s is performing %s' % (self.name, self.spawn_id, action))
        if action.__name__ == 'move':
            words = action.require['target'] + " " + str(action.require['pos_x']) + " " + str(action.require['pos_y'])
            self.tell(words)
            req=action.perform(self.spawn_id)
            self.comm_agents.send(req, who='core')
        elif action.__name__ == 'gather':
            words = action.require['target'] + " " + str(action.require['unit_tag'])
            self.tell(words)
            req=action.perform(self.spawn_id)
            self.comm_agents.send(req, who='core')
        elif action.__name__ == 'check':
            action.perform_query()
            return False
        else:
            print('act function --> else ERROR!!!!!!')
        return True

    def query(self, task_name, target, amount):
        #find knowledgebase

        if target in self.knowledge:
            current_amount = self.knowledge[target]['is']
            if current_amount >= amount:
                #knowledgebase update
                self.knowledge[task_name].update({'is': 'Done'})

    '''
        Delivering information to other agents
    '''
    def tell(self, statement):
        logger.info('%d is telling "%s" to the agents' % (self.spawn_id, statement))
        msg = str(self.spawn_id) + " is " + self.state.state
        print(">> {} is telling : {}".format(self.spawn_id, msg))
        self.comm_agents.send(msg, broadcast=True)


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
    def next_action(self, current_goal, current_knowledge, mentalstate):
        list_actions = []
        if len(current_goal) == 0:
            # TODO: is an action always triggered by a goal?
            return None, None

        # TODO: all the goals may need to be examined
        for goal in current_goal:
            # Method name is dirty
            leaf_goal, tasks = goal.get_available_goal_and_tasks()
            if len(tasks) != 0:
                leaf_goal.goal_state = 'assigned'
            for task in tasks:

                if mentalstate == 'idle':
                    #ping
                    if task.type == 'General':
                        if task.state == 'Ready' :
                           task.state = 'Ping'

                           #TODO - SangUk will do!
                           self.knowledge[task.__name__].update({'is' : [('Ping', self.spawn_id)]})

                        elif task.state == 'Ping' :
                            pinglist = self.knowledge[task.__name__]['is']

                            amImin = True
                            for ping in pinglist:
                                if self.spawn_id > ping[1]:
                                    amImin = False
                                    break

                            if amImin:
                                action = self._has_action_for_task(task)
                                if action is not None:
                                    list_actions.append((action, task))
                            else:
                                return None, None

                elif mentalstate == 'working':
                    if task.type == 'Query' and (task.state == 'Ready' or task.state == 'Active'):
                        #Check whether query task is done
                        action = self._has_action_for_task(task)
                        if action is not None:
                            list_actions.append((action, task))

        # Select actions from the list of actions in terms of the current
        if len(list_actions) == 0:
            return None, None

        return_action = list_actions[0]
        # Return the most beneficial action from the selected actions
        return return_action

    def update_goal_tree(self, knowledge, goal):

        if goal.name in knowledge:
            goal.goal_state = knowledge[goal.name]['is']

        # check subgoals
        for subgoal in goal.subgoals:
            self.update_goal_tree(knowledge, subgoal)


        # check task
        for task in self.tasks:
            if task.__name__ in knowledge:
                task.state = knowledge[task.__name__]['is']

        return True



    '''
        Main logic runs here (i.e., reasoning)
    '''
    def run(self):
        while self.alive:
            # For debugging
            logger.info('%s %d is ticking' % (self.name, self.spawn_id))
            print()

            for k in self.knowledge:
                print(k)


            # Check if something to answer
            # query = self.check_being_asked():
            # if query:
            #     self.answer(query)

            # Perceive environment
            self.perceive()

            #check knowledge and update the goal tree
            """
            tasks = []
            for g in self.goals:
                tasks = g.get_available_tasks()

            for k in self.knowledge:
                if k.type == 'type1':
                    for goal in self.goals:
                        if k.n == goal.name:
                            goal.goal_state = k.na
                    for task in tasks:
                        if k.n == task.__name__:
                            task.state = k.na
            """

            # check knowledge and update the goal tree
            for goal in self.goals:
                self.update_goal_tree(self.knowledge, goal)

            #check every goal whether now achieved.
            for goal in self.goals:
                goal.can_be_achieved() #check the goal state

            # Reason next action
            selected_action, selected_task = self.next_action(self.goals, self.knowledge, self.state.state)

            # Perform the action
            if selected_action is not None:
                if not self.act(selected_action, selected_task):
                    #Query task come here!
                    pass
                else:
                    #General task come here!
                    selected_task.state = 'Done'

            else:
                if self.goals[0].goal_state == 'achieved':
                    self.destroy()
                    break
                pass

            #TODO for Tony : Please Broadcast knowledge...
            time.sleep(self.discrete_time_step)



'''
    For testing
'''
if __name__ == '__main__':

    """
    goal = {'goal': 'introduce myself',
            'require': [
                ['say', {'words': 'hello'}],
                {'goal': 'say hello',
                 'require': [
                     ['say', {'words': 'myname'}],
                     ['say', {'words': 'hehe'}],
                     {'goal': 'say hajime',
                      'require': [
                          ['say', {'words': 'hajime'}]
                      ]}
                 ]
                 }
            ]
            }
    """

    goal = {'goal': 'gather 100 minerals',
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

    probe = Agent()
    probe.spawn(1,84,
        initial_knowledge=[
            ('type1', 'my_name', ['probe']),
            ('type2', 'i', 'say', ['my_name']),
            ],
        initial_goals=[create_goal_set(goal)]
        )
    print('Agent is running...')
    try:
        probe.run()
    except KeyboardInterrupt:
        pass
    probe.destroy()
    print('The agent is terminated.')
