"""
    Goal class
    This describes and stores (sub-)goals and their relationships
    Types,
        Conjunctive: achieving both sub goal A and B can attain the parent goal
        Disjunctive: achieving more than one of the sub goals satisfies attainment of the parent goal  
"""

'''
    Create a goal from a given description
    Format:
        <<goal>>::<<goal_name>>
                  <<require>>
                  <<precedent>>
        <<require>>::<<task>>
                     <<goal>>
    example: {'goal': 'say hello', 'require': [['say', 'hello']]}
'''
def create_goal_set(description_dict):
    assert 'goal' in description_dict

    g = Goal(description_dict['goal'])
    if 'require' in description_dict:
        dependents = description_dict['require']
        for dependent in dependents:
            if isinstance(dependent, list):  # Task
                g.set_required_task(Task(dependent[0], dependent[1]))
            elif isinstance(dependent, dict): # Goal
                pass
            else:
                pass
    else:
        # A goal with no tasks that satisfy it
        return None
    return g



class Goal(object):
    def __init__(self, goal_name=''):
        self.name = goal_name
        self.tasks = []
        self.dependents = []

    def __repr__(self):
        return '%s with %s tasks and %s dependents' % (self.name, self.tasks, self.dependents)

    def set_goal_name(goal_name):
        self.name = goal_name

    def set_required_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def get_goal(self):
        if len(self.goals) > 0:
            return self.goal[0]
        else:
            return None

class Task(object):
    def __init__(self, task_name='', arguments={}):
        self.__name__ = task_name
        self.arguments = arguments

    def __repr__(self):
        return '[Task \'%s\' with \'%s\']' % (self.__name__, self.arguments)

    def set_arguments(arguments):
        self.arguments = arguments
