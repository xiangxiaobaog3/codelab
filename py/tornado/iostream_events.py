# encoding: utf-8

import socket
from tornado import ioloop

def on_events(fd, events, error=None):
    if events & ioloop.IOLoop.READ:
        print("Socket read: %r" % fd.recv(1024))

    if events & ioloop.IOLoop.ERROR:
        print("Error received: %r" % error)

    if events & ioloop.IOLoop.WRITE:
        pass

_ioloop = ioloop.IOLoop.instance()
fd = socket.socket()
events_desired = ioloop.IOLoop.READ | ioloop.IOLoop.ERROR
_ioloop.add_handler(fd, on_events, events_desired)
_ioloop.start()
