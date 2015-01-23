#!/usr/bin/env python
# encoding: utf-8

# sending data over a stream but delimited as length-prefixed blocks

import socket, struct
from argparse import ArgumentParser

from utils import recvall


class DestinationError(Exception):
    def __str__(self):
        return "%s: %s" % (self.args[0], self.__cause__.strerror)


# message up to 2**32 - 1 (65535) in length
header_struct = struct.Struct('!I')
print("header_struct.size: %d" % header_struct.size)


def get_block(sock):
    data = recvall(sock, header_struct.size)
    (block_length, ) = header_struct.unpack(data)
    return recvall(sock, block_length)


def put_block(sock, message):
    block_length = len(message)
    sock.send(header_struct.pack(block_length))
    sock.send(message)


def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print("Run this script in another window with \"-c\" to connect")
    print("Listening at {}\n".format(sock.getsockname()))

    while True:
        sc, sockname = sock.accept()
        print("Accepted connection from {}".format(sockname))
        sc.shutdown(socket.SHUT_WR)

        while True:
            block = get_block(sc)
            if not block:
                break
            print("Block says:{}".format(repr(block)))

        sc.close()
        print("\n")
    sock.close()


def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    put_block(sock, b"Beautiful is better than ugly.\n")
    put_block(sock, b"Explicit is better than implicit.\n")
    put_block(sock, b"Simple is better than complex.\n")
    put_block(sock, b"")
    sock.close()


if __name__ == '__main__':
    parser = ArgumentParser(description='Transmit & receive a data stream')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                        help='IP address or hostname (default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', type=int, metavar='port', default=1060,
                        help='TCP port number (default: %(default)s)')
    args = parser.parse_args()
    function = client if args.c else server
    function((args.hostname, args.p))

