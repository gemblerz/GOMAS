#!/usr/bin/python3

"""
    Dummy Agent to test single agent using communicator.py
    This dummy communicates with the agent,
        - receive a message from the agent and check the agent's task
        - send a message(result) to the agent after checking the agent's message

    The agents need to change their goal state to Achieved/Failed state
    when the task is completed.

"""

import sys
import threading
import time
from datetime import datetime

sys.path.append('../')
from utils.communicator import Communicator, proxy


list_dummyname=[5501,5502,5503]
count_dummy=3



class DummyThread(threading.Thread):
    def __init__(self, name, counter):
        print(name+' Thread starts initializing...')

        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
        self.who=Dummy(self.name)
        self.who.init_comm_agents(self.name)

        print(self.name+' is Initialzied')

    def run(self):
        print(self.name+' is now running')
        cnt = 1
        wordorg="HI"
        while True:
            word=wordorg+' #'+str(cnt)
            if cnt == 20:
                #self.who.deinit_comm_agents()
                break

            #for i in range(count_dummy):


            # broadcasting
            addrs=[]
            for i in range(count_dummy):

                if list_dummyname[i]!=(self.threadID+5500):
                    addrs.append(list_dummyname[i])

            self.who.tell(word, addrs)

            cnt += 1
            print(cnt)

            for i in range(count_dummy):
                self.who.perceive()

            time.sleep(0.1)

        self.who.print_res()

class Dummy(object):
    def __init__(self,name):
        self.name=name
        self.count_sent=[0,0,0]
        self.count_recv=[0,0,0]
        self.filename_sent='dummy_log/'+name+'_sent.txt'
        self.filename_recv='dummy_log/'+name+'_recv.txt'
        self.file_sent=open(self.filename_sent,'w')
        self.file_recv=open(self.filename_recv,'w')
        self.id=int(''.join(x for x in name if x.isdigit()))+5500


    """
        Communication to other agents
    """

    def init_comm_agents(self, id):
        self.comm_agents = Communicator(self.id)


    def deinit_comm_agents(self):
        self.comm_agents.close()

    def perceive(self):
        message = self.comm_agents.read()
        if message:
            t=datetime.now()
            print(self.name+"\tGot message / Got Time: "+str(t)+" From\t" + message,file=self.file_recv)
            idx=''.join(x for x in message.split('/')[0] if x.isdigit())
            self.count_recv[int(idx)-1]+=1

    def tell(self, statement, who):
        t=datetime.now()
        msg=self.name+'/ Sent Time: '+str(t)+'/ Msg: '+statement
        print(self.name+"\tis telling to everyone "+msg,file=self.file_sent)
        #idx = who-5500#''.join(x for x in who if x.isdigit())
        for i in range(count_dummy):
            self.count_sent[i]+=1
        self.comm_agents.send(who, msg)

    def print_res(self):
        print(self.name)
        for i in range(count_dummy):
            print('\t'+self.name+' sent msg to \t\t%5d #: %d'%(i+1,self.count_sent[i]))
            print('\t'+self.name+' recv msg from \t%5d #: %d'%(i+1,self.count_recv[i]))

        self.file_sent.close()
        self.file_recv.close()



"""
    For testing
"""
if __name__ == '__main__':
    threads=[]

    #dummy1 = Dummy('dummy1')
    # dummy1 id = 'dummy1'
    #dummy1.init_comm_agents('dummy1')

    #dummy2 = Dummy('dummy2')
    # dummy2 id = 'dummy2'
    #dummy2.init_comm_agents('dummy2')

    #dummy3 = Dummy('dummy3')
    # dummy3 id = 'dummy3'
    #dummy3.init_comm_agents('dummy3')

    proxy_thread = threading.Thread(target=proxy)

    thread1=DummyThread('dummy1',1)
    thread2=DummyThread('dummy2',2)
    thread3=DummyThread('dummy3',3)

    time.sleep(1)

    proxy_thread.start()

    time.sleep(1) # wait for turn on proxy

    thread1.start()
    thread2.start()
    thread3.start()

    thread3.join()
    thread2.join()
    thread1.join()
