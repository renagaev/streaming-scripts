import threading
from store import store

class LampsSwitch:
    def __init__(self):
        self.lamps = [None for _ in range(5)]

    def on(self, index):
        print(f"on {index}")
        lamp = self.lamps[index]
        if lamp:
            lamp.on()

    def off(self, index, delay=0):
        print(f"off {index}, delay={delay}")
        lamp = self.lamps[index]
        if lamp:
            threading.Timer(delay, lamp.off).start()

    def set_state(self, index, value):
        lamp = self.lamps[index]
        if lamp:
            lamp.set_state(value)
