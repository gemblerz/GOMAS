import time

from agent import GorasAgent
import utils.goras_message_pb2 as msg_pb

class ListenerAgent(GorasAgent):
    def __init__(self):
        super().__init__(need_mouth=False, what_to_hear='units.4304666625.pos.*')

    def run(self):
        count = 0
        while not self.time_to_exit.is_set():
            sentence = self.hear()
            if sentence is not None:
                print(sentence)
            else:
                print('wy')
            time.sleep(0.1)

test = ListenerAgent()
try:
    test.start()
    test.join()
except:
    pass
test.terminate()