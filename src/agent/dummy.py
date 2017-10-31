#!/usr/bin/python3

"""
    Dummy Agent to test single agent using communicator.py
    This dummy communicates with the agent,
        - receive a message from the agent and check the agent's task
        - send a message(result) to the agent after checking the agent's message

    The agents need to change their goal state to Achieved/Failed state
    when the task is completed.

"""

import sys
import time
from agent import Agent
sys.path.append('../')
from utils.communicator import Communicator
from goal import create_goal_set
from utils.multithreading import AgentThread, DummyThread
import threading

class Dummy(object):
    def __init__(self):
        pass

    """
        Communication to other agents
    """

    def init_comm_agents(self, id):
        self.comm_agents = Communicator(id)


    def deinit_comm_agents(self):
        self.comm_agents.close()

    def perceive(self):
        message = self.comm_agents.read()
        print("Message from the Agent:" + message)
        if message:
            pass

    def tell(self, statement, who):
        print("Dummy is telling to the Agent")
        self.comm_agents.send(who, statement)


"""
    For testing
"""
if __name__ == '__main__':
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

    dummy = Dummy()
    # dummy id = 9999
    dummy.init_comm_agents('dummy')

    probe1 = Agent()
    probe2 = Agent()
    probe1.spawn(1, 84,
                initial_knowledge=[
                    ('type1', 'my_name', ['probe']),
                    ('type2', 'i', 'say', ['my_name']),
                ],
                initial_goals=[create_goal_set(goal)]
                )
    probe2.spawn(2, 84,
                 initial_knowledge=[
                     ('type1', 'my_name', ['probe']),
                     ('type2', 'i', 'say', ['my_name']),
                 ],
                 initial_goals=[create_goal_set(goal)]
                 )

    thread1=DummyThread("dummy",1,dummy)
    thread2=AgentThread("Agent",2,probe1)
    thread3=AgentThread("Agent",3,probe2)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()




