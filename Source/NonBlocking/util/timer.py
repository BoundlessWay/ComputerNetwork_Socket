#!/usr/bin/env python3
# timer.py

from threading import Thread, Event
from util.currency import fetch_latest

class TimerThread(Thread):
    def __init__(self, timeout):
        Thread.__init__(self)
        self.event = Event()
        self.timeout = timeout
        self.daemon=True
    def run(self):
        while not self.event.wait(self.timeout):
            fetch_latest()
            print("update!")
