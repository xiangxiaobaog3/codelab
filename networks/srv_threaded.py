#!/usr/bin/env python
# encoding: utf-8

# Using multiple threads to serve several clients in parallel.

import zen_utils
from threading import Thread


def start_threads(listener, workers=4):
    t = (listener, )
    for i in range(workers):
        Thread(target=zen_utils.accept_connections_forever, args=t).start()


def main():
    address = zen_utils.parse_command_line("Multi-threaded server")
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)

if __name__ == '__main__':
    main()
