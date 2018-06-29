
from agent import GorasAgent
import utils.goras_message_pb2 as msg_pb
import time
from pprint import pprint

class TestAgent(GorasAgent):
    def __init__(self):
        super().__init__(what_to_hear='resources.*')
        self.initialize_kb()

    def initialize_kb(self):
        self.kb = {}

    def ingest_belief(self, goras_message):

        if goras_message.WhichOneof('content') == 'inform':
            message_inform = goras_message.inform
            if message_inform.verb == 'is':
                key = message_inform.subject
                value = message_inform.object
                self.kb[key] = value
        else:
            print('wrong')

    def query_kb(self, query):
        pass

    def run(self):
        last_update_t = time.time()
        while True:
            message = self.hear()
            # print(message)
            # continue
            if message is not None:
                self.ingest_belief(message)
            current_t = time.time()
            if current_t - last_update_t > 1:
                pprint(self.kb)
                last_update_t = current_t
            time.sleep(0.5)


agent = TestAgent()
try:
    agent.run()
except (KeyboardInterrupt, Exception) as ex:
    print(str(ex))
finally:
    agent.terminate()