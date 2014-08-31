# encoding: utf-8

import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")
scrips = ['AAPL', 'GOOG', 'MSFT']


while True:
    scrip = random.choice(scrips)
    price = random.randrange(20, 700)
    msg = "%s: %s" % (scrip, price)
    print msg
    socket.send(msg)
    time.sleep(0.5)

