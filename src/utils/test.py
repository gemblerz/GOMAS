from rmq import RmqSubscriber

def callback(ch, method, properties, body):
    print(body)

try:
    with RmqSubscriber() as sub:
        sub.set_callback('log', callback)
        sub.begin_subscribe()
except KeyboardInterrupt:
    pass