# -*- coding: utf-8 -*-
# @Time    : 18-10-25 下午3:10
# @Author  : 张帆
# @Site    : 
# @File    : test2.py
# @Software: PyCharm
import argparse
import socket
import ssl


def client(host, port, cafile=None):
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    print(f"Connected to host {host} and port {port} ")
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    while True:
        data = ssl_sock.recv(1024)
        if not data:
            break
        print(repr(data))


def server(host, port, certfile, cafile=None):
    purpose = ssl.Purpose.CLIENT_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)
    context.load_cert_chain(certfile)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, port))
    listener.listen(1)
    print(f"Listening at inerface {host} and port {port}")
    raw_sock, address = listener.accept()
    print(f"connect from host {address[0]} and port {address[1]}")
    ssl_sock = context.wrap_socket(raw_sock, server_side=True)
    ssl_sock.sendall("Simple is better than complex.".encode("ascii"))
    ssl_sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Safe TLS client and server")
    parser.add_argument('host', help='hostname or iIP address')
    parser.add_argument('port', type=int, help='TCP port number')
    parser.add_argument('-a', metavar='cafile',default=None,help='authority:path to CA certificate PEM file')
    parser.add_argument('-s',metavar='certfile',default=None,help='run as server:path to server PEM file')
    args = parser.parse_args()
    if args.s:
        server(args.host,args.port,args.s,args.a)
    else:
        client(args.host,args.port,args.a)
