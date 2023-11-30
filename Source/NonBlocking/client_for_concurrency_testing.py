#!/usr/bin/env python3
import socket
import threading
import time


SOCKET_AMOUNT = 100
HOST, PORT = "localhost", 5566


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    while 1:
        sock.sendall(message.encode())
        time.sleep(1)
        # print(sock.recv(1024).decode())
    sock.close()


for i in range(SOCKET_AMOUNT):
    msg = "test message"
    client_thread = threading.Thread(target=client, args=(HOST, PORT, msg))
    client_thread.start()