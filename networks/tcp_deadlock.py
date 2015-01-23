#!/usr/bin/env python
# encoding: utf-8

# TCP client and server that leave too much data waitting


import sys, argparse, socket


def server(interface, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((interface, port))
    sock.listen(0)
    print("Listening at", sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print("Procssing up to 1024 bytes at a time from", sockname)
        n = 0
        while True:
            data = sc.recv(1024)
            if not data:
                break
            output = data.decode("ascii").upper().encode("ascii")
            sc.sendall(output) # send it back uppercase
            n += len(data)
            print("\r %d bytes processed so far" % (n, ))
            sys.stdout.flush()
        print()
        sc.close()
        print()
        print( "   Socket closed" )


def client(host, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bytecount = (bytecount + 5) // 16 * 16  # round up to a multiple of 16
    message = b'captialize this!' # 16-byte message to repeat over and over
    print("sending", bytecount, "bytes of data, in chunks of 16 bytes")
    sock.connect((host, port))
    sent = 0
    while sent < bytecount:
        sock.sendall(message)
        sent += len(message)
        print("\r %d bytes sent" % (sent, ))
        sys.stdout.flush()
    print()
    sock.shutdown(socket.SHUT_WR)
    print("Receiving all the data the server sends back")

    received = 0
    while True:
        data = sock.recv(42)
        if not received:
            print("  The first data received says", repr(data))
        if not data:
            break
        received += len(data)
        print("\r  %d bytes received" % (received, ))
    print()
    sock.close()


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Get deadlocked over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to',
                        default="127.0.0.1")
    parser.add_argument('bytecount', type=int, nargs='?', default=16,
                        help='number of bytes for client to send (default 16)')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p, args.bytecount)