"""
    Action class
    This lists all possible actions of a unit
    Actions can be performed under conditions and events
"""

class Action(object):
    def __init__(self, actions):
        self.action_set = {}
        for action in actions:
            self.action_set[action['id']] = {}
            self.action_set['name'] = action['name']
            self.action_set['require'] = action['require']

    '''
        Returns available actions based on the desires in the current situation
    '''
    def next_action(self, current_goal, current_knowledge):
        # List up possible actions that can achieve the goal

        # Select actions from the list of actions in terms of the current situation

        # Return the most beneficial action from the selected actions
        pass

