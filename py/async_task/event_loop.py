# encoding: utf-8

import select
import socket
import sys

host = ''
port = 5000
backlog = 5
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(backlog)

input_ = [server, sys.stdin]
running = 1

# the eventloop running
while running:
    inputready, outputready, exceptready = select.select(input_, [], [])
    print(inputready, outputready, exceptready)
    for s in inputready:
        if s == server:
            # handle the server socket
            client, address = server.accept()
            input_.append(client)
        elif s == sys.stdin:
            # handle standard input
            junk = sys.stdin.readline()
            running = 0
        else:
            # handle all other sockets
            data = s.recv(size)
            if data:
                s.send(data)
            else:
                s.close()
                input_.remove(s)

server.close()
