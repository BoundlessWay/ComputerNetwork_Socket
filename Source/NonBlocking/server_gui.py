#!/usr/bin/env python3
# server.py

import socket
import tkinter as tk
from threading import Thread
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL
from urllib.error import HTTPError
from util.loop_window import Loop
from util.currency import *
from util.user import *
from util.timer import TimerThread

LARGE_FONT = ("Bangers", 13, "bold")

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("PRO GUI")
        self.geometry("500x500")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=True, height=True)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        container.pack(side="top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
 
        self.frames = {}
        frame = ServerFrame(container, self)
        self.frames['serverFrame'] = frame 
        frame.grid(row=0, column=0, sticky="nsew")
 
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            s.close()
            self.destroy()

class ServerFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="RoyalBlue4")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0,1], weight=1)

        lbl_Title = tk.Label(self, text="SERVER LOG", font=LARGE_FONT,fg='floral white',bg="RoyalBlue4")
        lbl_Title.grid(row=0, column=0)
        
        global txt_Logging_Box
        txt_Logging_Box = tk.Text(self, width=60, borderwidth=3, relief=tk.SUNKEN, bg="white")
        txt_Logging_Box.grid(row=1, column=0, sticky="nsew")
        txt_Logging_Box.config(state=DISABLED)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=txt_Logging_Box.yview)
        scrollbar.grid(row=1, column=1, sticky='news')
        txt_Logging_Box['yscrollcommand'] = scrollbar.set

 
    def logging(msg):
        txt_Logging_Box.config(state=NORMAL)
        txt_Logging_Box.insert(tk.END, msg)
        txt_Logging_Box.config(state=DISABLED)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5566))
s.listen(10240)
s.setblocking(False)

loop = Loop()

MAN_SHELL = "0"
MAN_LATEST ="0"
MAN_HISTORICAL = "0"
MAN_CONVERT = "0"
MAN_TIMESERIES = "0"
MAN_LOGIN = "0"
MAN_REGISTER = "0"
MAN_QUIT = "0"

def interpret(msg, addr):
    if not msg:
        return MAN_SHELL

    msg = msg.split()

    if msg[0] == 'latest':
        try:
            data = latest(msg[1:])
            msg = json.dumps(data, indent=2)
            ServerFrame.logging(repr(addr) + ' use latest\n')  # log this
        except KeyError:
            msg = MAN_LATEST

    elif msg[0] == 'historical':
        try:
            data = historical(msg[1], msg[2:])
            msg = json.dumps(data, indent=2)
            ServerFrame.logging(repr(addr) + ' historical\n')  # log this
        except (KeyError, IndexError, HTTPError):
            msg = MAN_HISTORICAL

    elif msg[0] == 'convert':
        try:
            msg = str(convert(msg[1], msg[2], msg[3], msg[4]))
            ServerFrame.logging(repr(addr) + ' convert\n')  # log this
        except IndexError:
            try:
                msg = str(convert(msg[1], msg[2], msg[3]))
                ServerFrame.logging(repr(addr) + ' convert\n')  # log this
            except (KeyError, IndexError, ValueError):
                msg = MAN_CONVERT

    elif msg[0] == 'timeseries':
        try:
            data = timeseries(msg[1], msg[2], msg[3:])
            msg = json.dumps(data, indent=2)
            ServerFrame.logging(repr(addr) + ' use timeseries\n')  # log this
        except:
            try:
                data = timeseries(msg[1], msg[2])
                msg = json.dumps(data, indent=2)
                ServerFrame.logging(repr(addr) + ' use timeseries\n')  # log this
            except (KeyError, IndexError, HTTPError):
                msg = MAN_TIMESERIES

    elif msg[0] == 'logout':
        msg = 'Logging out'
    elif msg[0] == 'quit':
        msg = 'Quitted'
    else:
        msg = MAN_SHELL
    return msg

def interpret_before_handler(msg, addr):
    if not msg:
        return MAN_LOGIN

    msg = msg.split()
    if msg[0] == 'register':
        try:
            msg = register(msg[1], msg[2])
            if msg:
                msg = 'Account successfully registered'
            else:
                msg = 'Account already exists'
        except IndexError:
            msg = MAN_REGISTER   
    elif msg[0] == 'login':
        try:
            msg = login(msg[1], msg[2])
            if msg:
                msg = 'True'   # success
            else:
                msg = 'Username or password incorrect!'    
        except IndexError:
            msg = MAN_LOGIN    # wrong syntax
    elif msg[0] == 'quit':
        msg = 'Quitted'
    else:
        msg = 'You must login first!\n' + MAN_LOGIN
    return msg

def handler(conn, addr):
    logout = False
    while not logout:
        msg = yield from loop.recv(conn, 1642500)
        if not msg:
            conn.close()
            break
        msg = interpret(msg.decode(), addr)
        if msg == 'Quitted':
            ServerFrame.logging(repr(addr) + ' quitted\n')  # log this
            yield from loop.send(conn, msg.encode())
            conn.close()
            break
        elif msg == 'Logging out':
            ServerFrame.logging(repr(addr) + ' logging out\n')  # log this
            loop.create_task((before_handler(conn,addr), None))
            logout = True

        yield from loop.send(conn, msg.encode())

def before_handler(conn, addr):
    logged = False
    while not logged:
        msg = yield from loop.recv(conn, 1024)
        if not msg:
            conn.close()
            break
        msg = interpret_before_handler(msg.decode(), addr)
        if msg == 'Quitted':
            ServerFrame.logging(repr(addr) + ' quitted\n')  # log this
            yield from loop.send(conn, msg.encode())
            conn.close()
            break
        elif msg == 'Account successfully registered':
            ServerFrame.logging(repr(addr) + ' registered an account\n')    # log this
        elif msg == 'True':
            msg = 'Logged in successfully'
            ServerFrame.logging(repr(addr) + ' logged in\n')    # log this
            loop.create_task((handler(conn, addr), None))
            logged = True
        msg = msg.encode()
        yield from loop.send(conn, msg)

conns = []

def main():
    while True:
        conn, addr = yield from loop.accept(s)
        conns.append(conn)
        ServerFrame.logging(repr(addr) + ' connected\n')    # log this
        conn.setblocking(False)
        loop.create_task((before_handler(conn, addr), None))

def close_cuc_suc():
    for conn in conns:
        conn.close()

class ServerGUIThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
    def run(self):
        app = App()
        app.mainloop()



# global gui
# global timer
gui = ServerGUIThread()     # maintain GUI
gui.start()
timer = TimerThread(1800)   # maintain timer for database updating every 30 minutes
timer.start()
loop.create_task((main(), None))
loop.run()
