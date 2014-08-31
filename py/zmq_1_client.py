# encoding: utf-8

import zmq
import time

context = zmq.Context()

# Socket to talk to server
print("Connecting to hello world server")

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# DO 10 requests, waitting each time for a response
for req_no in range(10):
    socket.send("Hello")

    # Get the reply.
    message = socket.recv()
    print("Received reply ", req_no, "[", message, "]")
    time.sleep(1)


