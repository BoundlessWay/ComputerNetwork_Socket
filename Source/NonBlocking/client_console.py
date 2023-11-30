#!/usr/bin/env python3
# client_console.py
import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5566))

while True:
    msg = input("$ ")
    if not msg:
        continue
    try:
        s.send(msg.encode())
        msg = s.recv(1700000).decode()
    except BrokenPipeError:
        break
    print(msg)