import sys
import threading
import time
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

class DummyThread(threading.Thread):
    def __init__(self, name, counter,who):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
        self.who=who

    def run(self):
        cnt = 1
        word = "I'm DUMMY"
        while True:
            if cnt == 20:
                self.who.deinit_comm_agents()
                break

            self.who.tell(word, 1)
            time.sleep(0.1)
            self.who.perceive()

            cnt += 1
