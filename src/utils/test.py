from rmq import RmqSubscriber
import time

ear = RmqSubscriber.default('*')

try:
    while True:
        print(ear.read())
        time.sleep(1)
except:
    ear.close()