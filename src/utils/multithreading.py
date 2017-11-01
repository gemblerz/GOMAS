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

list_dummyname=['dummy1','dummy2','dummy3']
count_dummy=3
class DummyThread(threading.Thread):
    def __init__(self, name, counter,who):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
        self.who=who

    def run(self):
        cnt = 1
        wordorg="HI"
        while True:
            word=wordorg+' #'+str(cnt)
            if cnt == 10:
                self.who.deinit_comm_agents()
                break
            for i in range(count_dummy):
                self.who.perceive()

            # broadcasting
            for i in range(count_dummy):

                if list_dummyname[i]!=self.name:
                    self.who.tell(word, list_dummyname[i])

            cnt += 1

            time.sleep(1)
