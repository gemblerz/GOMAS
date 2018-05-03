import time

from agent import GorasAgent
import utils.goras_message_pb2 as msg_pb

class TestAgent(GorasAgent):
    def __init__(self):
        super().__init__(need_mouth=True, need_ears=False)

    def run(self):
        count = 0
        while not self.time_to_exit.is_set():
            query = msg_pb.GorasQuery(question='create_game')
            sentence = msg_pb.GorasSentence(id=count, speaker='testagent', query=query)
            print(sentence)
            self.mouth.say('sim', sentence.SerializeToString())
            a = input("wait")
            print(sentence)
            count += 1
            if count >= 1000:
                return
            time.sleep(1)

test = TestAgent()
try:
    test.start()
    test.join()
except:
    pass
test.terminate()