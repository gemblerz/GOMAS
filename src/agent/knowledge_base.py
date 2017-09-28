"""
    Knowledge base class
    This stores statements formed from observations/communications
    Atomic forms are
        none, none/adjective                e.g., (apple, red)
        none, verb [objective]              e.g., (probe, gather, the mineral)
        verb, (none/verb none/adjective)    e.g., (attack, (target, hurt)), (attack, (drain, my_energy))
"""

class Knowledge(object):
    def __init__(self, initial_knowledge=[]):
        self.knowledge = []
        for entity in initial_knowledge:
            self.knowledge = entity

    '''
        Returns list of the statements
    '''
    def list(self):
        pass