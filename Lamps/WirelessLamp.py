from queue import Queue
from threading import Thread

from Lamps.lamp import Lamp
from gadgets.NodeMCU import NodeMCU
from time import sleep


class WirelessLamp(Lamp):
    def __init__(self, ip):
        self.nodemcu = NodeMCU(ip)
        self.queue = Queue()
        Thread(target=self._consume).start()
        self.queue.put((3,0))

    def off(self):
        self.queue.put((2, 0,))

    def on(self):
        self.queue.put((2, 1,))

    def _consume(self):
        while True:
            while not self.queue.empty():
                pin, value = self.queue.get()
                self.nodemcu.send(pin, value)
                self.queue.task_done()
            sleep(0.05)
