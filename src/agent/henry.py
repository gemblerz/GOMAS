#!/usr/bin/python3

"""
    Dummy Agent to test single agent using communicator.py
    This dummy communicates with the agent,
        - receive a message from the agent and check the agent's task
        - send a message(result) to the agent after checking the agent's message

    The agents need to change their goal state to Achieved/Failed state
    when the task is completed.

"""


from knowledge_base import Knowledge

"""
    For testing
"""
if __name__ == '__main__':

	temp = Knowledge()
	temp['has']={'i':'temp'}
	dict1= {'I' : {'am' : []}}
	dict2= {'I' : {'am' : [('hey','here')]}}
	dict3={'you' : {'are' : '30'}}
	dict4={'I' : {'am' : ['testing']}}

	temp.update(dict1)
	temp.update(dict2)
	temp.update(dict3)
	temp.update(dict4)
	print(temp)
