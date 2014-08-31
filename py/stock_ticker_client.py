# encoding: utf-8

import sys
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting updates from stock server..."
socket.connect("tcp://localhost:5556")

scrip_filter = sys.argv[1:] if len(sys.argv) > 1 else ["AAPL"]

for scrip in scrip_filter:
    socket.setsockopt(zmq.SUBSCRIBE, scrip)

while True:
    s = socket.recv()
    stock, price = s.split()
    print "%s: %s" % (stock, price)
