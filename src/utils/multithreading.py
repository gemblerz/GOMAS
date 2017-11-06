import sys
import threading
import time
from datetime import datetime

sys.path.append('../')

class AgentThread(threading.Thread):

    def __init__(self, name, counter,who):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
        self.who=who

    def run(self):
        print('Agent is running...')
        try:
            self.who.run()
        except KeyboardInterrupt:
            pass
        self.who.destroy()
        print('The agent is terminated.')

