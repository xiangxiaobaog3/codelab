import zmq

context = zmq.Context()

responder = context.socket(zmq.REP)
responder.bind("tcp://*:5555")

# block until recv
request = responder.recv(0)
responder.send("Heoo", 0)

