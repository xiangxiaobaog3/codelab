#!/usr/bin/env python
# encoding: utf-8

import socket

hostname = 'www.python.org'
addr = socket.gethostbyname(hostname)
print('the ip address of {} is {}'.format(hostname, addr))
