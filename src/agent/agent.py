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

from utils.jsonencoder import PythonObjectEncoder,as_python_object

FORMAT = '%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

task_state={'Ready':0,'Ping':1,'Active':2,'Done':3}
goal_state={'Not Assigned':0,'assigned':1,'active':2,'achieved':3}

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

        self.discrete_time_step = 0.5  # sec
        self.alive = False
        self.state = MentalState()

        self.actions = get_basic_actions()
        self.knowledge = Knowledge()
        self.goals = []
        self.messages = []

    def _load_knowledge(self, knowledge):
        for key, value in knowledge.items():
            self.knowledge[key] = value
            # self.tuple_to_knowledge(k)
            # self.knowledge.append(k)

    def _load_goals(self, goals):
        self.goals = goals

    def spawn(self, spawn_id, unit_id, initial_knowledge={}, initial_goals=[]):
        logging.info(str(spawn_id) + ' is being spawned...')

        assert unit_id in units

        # Identifier for the unit
        self.spawn_id = spawn_id
        print("{} is spawned".format(spawn_id))

        # Load basic characteristics of the unit
        self.load_unit(units[unit_id])

        # Set initial statements in knowledge
        self._load_knowledge(initial_knowledge)
        print(self.knowledge)

        # Store initial goals
        self._load_goals(initial_goals)

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
        # self.comm_agents = Communicator(self.spawn_id)
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
            message = message[13:]
            self.knowledge.update(json.loads(message,object_hook=as_python_object))

    '''
        Information / actions going to simulator
    '''

    def act(self, action, task):
        self.state.change_state()

        # Update task state
        if self.knowledge[task.__name__]['is'] == task_state['Active'] - 1:
            self.knowledge[task.__name__].update({'is': task_state['Active']})

            # logger.info('%s %s is performing %s' % (self.name, self.spawn_id, action))
            self.log('%s %s is performing %s' % (self.name, self.spawn_id, action))
            if action.__name__ == 'move':
                req = action.perform(self.spawn_id)
                self.comm_agents.send(req, who='core')
            elif action.__name__ == 'gather':
                req = action.perform(self.spawn_id)
                self.comm_agents.send(req, who='core')
            elif action.__name__ == 'build_pylon':
                req = action.perform(self.spawn_id)
                self.comm_agents.send(req, who='core')
            elif action.__name__ == 'check':
                self.query(task.__name__, task.arguments['target'], task.arguments['amount'])
                # action.perform_query()
                return False
            else:
                print('act function --> else ERROR!!!!!!')
            return True
        return False

    def query(self, task_name, target, amount):
        # find knowledgebase

        if target in self.knowledge:
            if target == 'minerals':
                current_amount = self.knowledge[target]['gathered']
                if int(current_amount) >= int(amount):
                    # print("성취됨!!!!!!!!!!!!!")
                    #knowledgebase update
                    self.knowledge[task_name].update({'is': task_state['Done']})
                    self.state.__init__()
            elif target == 'pylons':
                current_amount = self.knowledge[target]['built']
            else: return

            if int(current_amount) >= int(amount):
                # print("성취됨!!!!!!!!!!!!!")
                # knowledgebase update
                self.knowledge[task_name].update({'is': task_state['Done']})
                self.state.__init__()

    '''
        Delivering information to other agents
    '''

    def tell(self, statement):
        #logger.info('%d is telling "%s" to the agents' % (self.spawn_id, statement))
        self.log('%d is telling "%s" to the agents' % (self.spawn_id, statement))
        #msg = str(self.spawn_id) + " is " + self.state.state
        #print(">> {} is telling : {}".format(self.spawn_id, statement))
        self.comm_agents.send(statement, broadcast=True)

    def log(self, message):
        self.comm_agents.log(message, str(self.spawn_id))
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

    """
        Check the goal tree recursively and update KB if it is achieved.
    """

    def check_goal_achieved(self, goal):
        if goal is not None:
            if goal.can_be_achieved():
                print('뭐 좀 찍어볼까?????')
                self.knowledge[goal.name].update({'is': 'achieved'})
                print(goal.name)
                print(self.knowledge[goal.name]['is'])
            for subgoal in goal.subgoals:
                if subgoal.can_be_achieved():
                    print('뭐 좀 찍어볼까?????')
                    self.knowledge[subgoal.name].update({'is': 'achieved'})
                    print(subgoal.name)
                    print(self.knowledge[subgoal.name]['is'])
                    self.check_goal_achieved(subgoal)
        return None

    '''
        Returns available actions based on the desires in the current situation
    '''

    def next_action(self, current_goal, current_knowledge, mentalstate):
        list_actions = []
        print("####NEXT_ACTION: CURRENT GOAL's length: %s" % (len(current_goal)))
        if len(current_goal) == 0:
            # TODO: is an action always triggered by a goal?
            return None, None

        # TODO: all the goals may need to be examined
        for goal in current_goal:
            # Method name is dirty
            leaf_goal, tasks = goal.get_available_goal_and_tasks()
            # When the Query task is Done, the agent's mentalstate is Idle
            for task in tasks:
                if task.type == 'Query' and self.knowledge[task.__name__]['is'] == task_state['Done']:
                    self.state.__init__()
            if len(tasks) != 0:
                if leaf_goal.goal_state != 'achieved':
                    leaf_goal.goal_state = 'assigned'
                    self.knowledge[leaf_goal.name].update({'is': 'assigned'})
            for task in tasks:

                if mentalstate == 'idle':
                    # ping
                    if task.type == 'General':
                        if task.state == task_state['Ready']:
                            task.state = task_state['Ping']
                            pinglist = set()
                            pinglist.add(self.spawn_id)
                            self.knowledge[task.__name__].update({'is': task_state['Ping']})
                            self.knowledge[task.__name__].update({'ping': pinglist})

                            '''
                            #TODO - SangUk will do!
                            self.knowledge[task.__name__].update({'is' : ('Ping', self.spawn_id)})
                            '''
                            break

                        elif task.state == task_state['Ping']:
                            pinglist = self.knowledge[task.__name__]['ping']

                            amImin = True
                            for ping in pinglist:
                                if int(self.spawn_id) > int(ping):
                                    amImin = False
                                    break

                            if amImin:
                                if int(self.spawn_id) not in pinglist:
                                    pinglist.add(self.spawn_id)
                                self.knowledge[task.__name__].update({'ping' : pinglist})

                                action = self._has_action_for_task(task)
                                if action is not None:
                                    list_actions.append((action, task))
                                    break
                            else:
                                return None, None

                        elif task.state == task_state['Active']:
                            return None, None

                elif mentalstate == 'working':
                    if task.type == 'Query' and (task.state == task_state['Ready'] or task.state == task_state['Active']):
                        # Check whether query task is done
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
            if goal.goal_state != 'achieved':
                goal.goal_state = knowledge[goal.name]['is']

        # check subgoals
        for subgoal in goal.subgoals:
            self.update_goal_tree(knowledge, subgoal)

        # check task
        for task in goal.tasks:
            if task.__name__ in knowledge:
                #print("!!", self.spawn_id, task.__name__, task.state, "-->", knowledge[task.__name__]['is'])
                if knowledge[task.__name__]['is'] == task_state['Done']:
                    knowledge[task.__name__]['ping'] = []
                task.state = knowledge[task.__name__]['is']

        return True

    '''
        Main logic runs here (i.e., reasoning)
    '''

    def run(self):
        # Initialize communications
        self.init_comm_env()
        self.init_comm_agents()

        while self.alive:
            # For debugging
            logger.info('%s %d is ticking' % (self.name, self.spawn_id))
            # print()

            # for k in self.knowledge:
            #     print(k)
            #print(self.knowledge)
            print(self.state)

            # Check if something to answer
            # query = self.check_being_asked():
            # if query:
            #     self.answer(query)

            # Perceive environment
            self.perceive()
            self.perceive()
            self.perceive()
            self.perceive()
            self.perceive()
            self.log(json.dumps(self.knowledge,cls=PythonObjectEncoder))

            #check knowledge and update the goal tree=
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


            # check every goal whether now achieved.
            for goal in self.goals:
                self.check_goal_achieved(goal)
                if goal.can_be_achieved(): #check the goal state
                    # print('뭐 좀 찍어볼까?????')
                    self.knowledge[goal.name].update({'is' : 'achieved'})
                    # print(self.knowledge[goal.name]['is'])

            # Reason next action
            selected_action, selected_task = self.next_action(self.goals, self.knowledge, self.state.state)
            # print(self.spawn_id, "다음은!!! ", selected_action, selected_task)
            # Perform the action
            if selected_action is not None:
                if not self.act(selected_action, selected_task):
                    # Query task come here!
                    pass
                else:
                    # General task come here!
                    selected_task.state = task_state['Done']
                    self.knowledge[selected_task.__name__]['ping'] = self.spawn_id
                    self.knowledge[selected_task.__name__].update({'is': task_state['Done']})
                    # Have to change agent's state to idle after finishing the task
                    # self.state.__init__()

            else:
                # print('다 됐다!!!!!!!!!!!!!!!!!!!')
                if self.goals[0].goal_state == 'achieved':
                    # print('여기 들어옴?? ???????')
                    for act in self.actions:
                        if act.__name__ == 'move':
                            req=act.perform(self.spawn_id)
                            self.comm_agents.send(req,who='core')

                    # self.destroy()
                    # break
                pass

            # TODO for Tony : Please Broadcast knowledge...
            self.tell(json.dumps(self.knowledge,cls=PythonObjectEncoder))

            time.sleep(self.discrete_time_step)