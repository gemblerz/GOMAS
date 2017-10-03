"""
    Goal class
    This describes and stores (sub-)goals and their relationships
    Types,
        Conjunctive: achieving both sub goal A and B can attain the parent goal
        Disjunctive: achieving more than one of the sub goals satisfies attainment of the parent goal  
"""

class Goal(object):
    def __init__(self, initial_goals):
        self.goals = initial_goals

    def get_goals(self):
        # returns all available goals/sub-goals
        return self.goals

    def get_goal(self):
        if len(self.goals) > 0:
            return self.goal[0]
        else:
            return None