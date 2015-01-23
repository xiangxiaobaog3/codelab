#!/usr/bin/env python
# encoding: utf-8


# send a big UDP datagram to learn the MTU of the network path

import IN, argparse, socket

if not hasattr(IN, 'IP_MTU'):
    raise RuntimeError("cannot perform MTU discovery on this combination"
                       " of operating system and Python distribution")


def send_big_datagram(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, IN.IP_MTU_DISCOVER, IN.IP_PMTUDISC_DO)
    socket.connect((host, port))
    try:
        sock.send(b"#" * 65000)
    except socket.error:
        print("Alas, the datagram did not make it")
        max_mtu = sock.getsocketopt(socket.IPPROTO_IP, IN.IP_MTU)
        print("Actual MTU: {}".format(max_mtu))
    else:
        print("The big datagram was sent!")


def main():
    parser = argparse.ArgumentParser(description="Send UDP packet to get MTU")
    parser.add_argument("host", help="the host to which to target the packet")
    parser.add_argument("-p", metavar="PORT", type=int, default=1060,
                        help="UDP port")
    args = parser.parse_args()
    send_big_datagram(args.host, args.p)


if __name__ == '__main__':
    main()
