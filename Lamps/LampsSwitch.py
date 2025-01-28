import threading
from typing import List
from store import store
from Lamps.lamp import Lamp


class LampsSwitch:
    def __init__(self):
        self.lamps: List[Lamp] = [None for _ in range(5)]

    def on(self, index):
        lamp = self.lamps[index]
        if lamp:
            lamp.on()

    def off(self, index, delay=0):
        lamp = self.lamps[index]
        if lamp:
            threading.Timer(delay, lamp.off).start()

    def on_green(self, index):
        lamp = self.lamps[index]
        if lamp:
            lamp.on_green()

    def off_green(self, index):
        lamp = self.lamps[index]
        if lamp:
            lamp.off_green()

    def set_state(self, index, value):
        lamp = self.lamps[index]
        if lamp:
            lamp.set_state(value)
