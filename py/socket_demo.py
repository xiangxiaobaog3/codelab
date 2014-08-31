#!/usr/bin/env python
# encoding: utf-8

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("g.cn", 80))

# Create an INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 8001)) # bind
# become a server socket
server_socket.listen(5)

def client_thread(clientsocket):
    print("enter a client thread")
    data = clientsocket.recv(100)
    print("received data:", data)
    clientsocket.send(data.upper())

(clientsocket, address) = server_socket.accept()
print(clientsocket, address)
while True:
    client_thread(clientsocket)

server_socket.close()
