import time

from utils.rmq import RmqSubscriber
from agent import GorasAgent


class GorasLogger(GorasAgent):
    def __init__(self):
        super().__init__(need_ears=True, what_to_hear='log')
        self.history_path = '/tmp/simulation.history'

    def terminate(self):
        super().terminate()

    def run(self):
        with open(self.history_path, 'w') as log:
            while not self.time_to_exit.is_set():
                message = self.ears.hear()
                if message is not None:
                    print(message)
                    sentence = self.interpret(message)
                    print(sentence)
                    # timestamp, body = message
                    # tiemstamp /= 1000
                    # formatted = '{},{}'.format(timestamp, body)
                    # log.write(formatted)
                else:
                    time.sleep(0.1)

logger = GorasLogger()
try:
    logger.start()
    logger.join()
except:
    pass
logger.terminate()