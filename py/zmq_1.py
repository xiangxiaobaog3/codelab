# encoding: utf-8

import zmq

context = zmq.Context()

print("Starting hello world server...")

socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print("Got: ", message)

    # Send the reply.
    socket.send("World")
