import time

import sys

from agent import GorasAgent
import utils.goras_message_pb2 as msg_pb

class ListenerAgent(GorasAgent):
    def __init__(self, what_to_hear='*'):
        super().__init__(need_mouth=False, what_to_hear=what_to_hear)

    def run(self):
        count = 0
        while not self.time_to_exit.is_set():
            sentence = self.hear()
            if sentence is not None:
                print(sentence)
            else:
                print('wy')
            time.sleep(0.1)
            
test = ListenerAgent(sys.argv[1])
try:
    test.start()
    test.join()
except:
    pass
test.terminate()