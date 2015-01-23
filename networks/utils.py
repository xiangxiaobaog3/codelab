#!/usr/bin/env python
# encoding: utf-8


def recvall(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError("socket closed with %d bytes left"
                           " in this block.".format(length))
        length -= len(block)
        blocks.append(block)
    return b"".join(blocks)
