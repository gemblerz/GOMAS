from threading import Thread, Event


class GorasAgent(Thread):
    def __init__(self):
        super().__init__()
        self.time_to_exit = Event()
        self.time_to_exit.clear()

    def terminate(self):
        self.time_to_exit.set()
        self.join()

    def run(self):
        raise NotImplemented('run method must exist')