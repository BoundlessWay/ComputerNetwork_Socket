#!/usr/bin/env python3
# loop_window.py

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
import time

class Loop(object):
    """
    Loop object that can handle tasks efficiently, and easy to read
    """
    def __init__(self):
        self.sel = DefaultSelector()
        self.queue = []

    def create_task(self, task):
        """
        Append task to queue
        """
        self.queue.append(task)

    def polling(self):
        """
        Fetch all IO objs ready for IO from selectors pool, append to queue
        """
        while True:
            try: 
                time.sleep(0.00001)
                e, m = self.sel.select(0)
                self.queue.append((e.data, None))
            except:
                break

    def is_registered(self, fileobj):
        """
        Check if obj is registered or not
        """
        try:
            self.sel.get_key(fileobj)
        except KeyError:
            return False
        return True

    def register(self, t, data):
        """
        Register IO objs
        """
        if not data:
            return False

        if data[0] == EVENT_READ:
            if self.is_registered(data[1]):
                self.sel.modify(data[1], EVENT_READ, t)
            else:
                self.sel.register(data[1], EVENT_READ, t)
        elif data[0] == EVENT_WRITE:
            if self.is_registered(data[1]):
                self.sel.modify(data[1], EVENT_WRITE, t)
            else:
                self.sel.register(data[1], EVENT_WRITE, t)
        else:
            return False

        return True

    def accept(self, s):
        """
        If successfully accept then return (conn, addr). 
        If there're no conections then send data back to caller.
        """
        conn, addr = None, None
        while True: # cho nay k co while chay khong duoc :)) 
            try:
                conn, addr = s.accept()
            except (BlockingIOError, OSError):
                yield (EVENT_READ, s)
            else:
                break
        return conn, addr


    def recv(self, conn, size):
        """
        If we got the msg or connection is down then return msg. 
        If we haven't got the msg yet (BlockingIOError) then send data back to caller.
        """
        msg = None
        while True:
            try:
                msg = conn.recv(size)
            except BlockingIOError:
                yield (EVENT_READ, conn)
            else:
                break
        return msg

    def send(self, conn, msg):
        """
        - If we successfully sent the msg or connection is down, then return size. 
        - If msg haven't been sent yet (BlockingIOError) then send data back to caller.
        """
        size = 0
        while True:
            try:
                size = conn.send(msg)
            except BlockingIOError:
                yield (EVENT_WRITE, conn)
            else:
                break
        return size

    def once(self):
        """
        Polling all available IO objs to task queue, then send data to generator and let them do the job. 
        When job is done and we have data returned back then register to monitor IO. Gather unfinished tasks for a new task queue. 
        If StopIteration exception raised then continue without registering because there're nothing to register.
        """
        self.polling()
        unfinished = []
        for t, data in self.queue:
            try:
                data = t.send(data)
            except StopIteration:
                continue

            if self.register(t, data):
                unfinished.append((t, None))

        self.queue = unfinished

    def run(self):
        while self.queue or self.sel.get_map():
            self.once()
