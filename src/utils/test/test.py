import new_communicator

test= new_communicator.Communicator(5000)
test.connect(5000)
for num in range(5):
    test.send()
    test.receive()
test.end()

