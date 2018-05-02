from utils.rmq import RmqSubscriber
from goras_agent import GorasAgent


class GorasLogger(GorasAgent):
    def __init__(self):
        super().__init__()
        self.history_path = '/tmp/simulation.history'
        self.ear = RmqSubscriber.default(what_to_hear='log')

    def terminate(self):
        super().terminate()
        self.ear.close()

    def run(self):
        with open(self.history_path, 'w') as log:
            while not self.time_to_exit.is_set():
                message = self.ear.hear()
                if message is not None:
                    timestamp, body = message
                    tiemstamp /= 1000
                    formatted = '{},{}'.format(timestamp, body)
                    log.write(formatted)
                time.sleep(0.1)
