#!/usr/bin/env python
# encoding: utf-8

import sys
import zmq


context = zmq.Context()
socket = context.socket(zmq.SUB)


print("Collecting updates from weather server...")
socket.connect("tcp://localhost:5556")

# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[1] if len(sys.argv) > 1 else '10001'

# to unicode
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')

socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

# Process 5 updates
total_temp = 0

for update_nbr in range(5):
    string = socket.recv_string()
    zipcode, temperature, relhumidity = string.split()
    print(zipcode, temperature, relhumidity)
    total_temp += int(temperature)

print("Average temperature for zipcode '%s' was %dF" % (
    zip_filter, total_temp/update_nbr
))
