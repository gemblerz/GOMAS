import time

from agent import GorasAgent
import utils.goras_message_pb2 as msg_pb

class TestAgent(GorasAgent):
    def __init__(self):
        super().__init__(need_mouth=True, need_ears=False)

    def run(self):
        count = 0
        while not self.time_to_exit.is_set():
            query = msg_pb.GorasCommand(action='start_game')
            print(query)
            self.say('sim', query)
            a = input("wait")
            break

test = TestAgent()
try:
    test.start()
    test.join()
except:
    pass
test.terminate()