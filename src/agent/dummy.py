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
import logging
sys.path.append('../')
from utils.communicator import Communicator

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
    dummy = Dummy()
    # dummy id = 9999
    dummy.init_comm_agents(9999)
    cnt = 1
    word = "Hello"
    while True:
        if cnt == 10:
            dummy.deinit_comm_agents()
            break
        dummy.tell(word, "84")
        time.sleep(1)
        dummy.perceive()
        cnt += 1
