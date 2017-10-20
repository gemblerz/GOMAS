import zmq
import time

def main():
    context = zmq.Context()
    ssocket = context.socket(zmq.SUB)
    ssocket.bind('tcp://127.0.0.1:5000')
    psocket = context.socket(zmq.PUB)
    psocket.connect('tcp://127.0.0.1:5000')

    ssocket.setsockopt_string(zmq.SUBSCRIBE, '')

    for i in range(3):
        time.sleep(0.1)
        try:
            ssocket.recv(zmq.NOBLOCK)
        except:
            pass
    psocket.send_string('hello')
    print(ssocket.recv_string())

if __name__ == '__main__':
    main()

