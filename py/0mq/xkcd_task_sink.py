# encoding: utf-8

import zmq

context = zmq.Context()

receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

while True:
    s = receiver.recv()
    print s
