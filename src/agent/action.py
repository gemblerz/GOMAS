"""
    Action class
    This lists all possible actions of a unit
    Actions can be performed under conditions and events
"""


'''
    Returns basic acitons of an agent
'''
def get_basic_actions():
    actions = []
    actions.append(Action(action_name='say', require={'words': 'string'}))
    return actions


class Action(object):
    def __init__(self, action_name, require={}, sc_action_id=9999):
        self.__name__ = action_name
        self.sc2_id = sc_action_id
        self.require = require