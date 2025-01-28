from queue import Queue
from threading import Thread

from Lamps.lamp import Lamp
from gadgets.NodeMCU import NodeMCU
from time import sleep


class WirelessLamp(Lamp):
    def __init__(self, ip):
        self.nodemcu = NodeMCU(ip)
        self.queue = Queue()
        self.state = "red_off"
        Thread(target=self._consume).start()
        Thread(target=self.renew).start()

    def off(self):
        self.state = "red_off"
        self.queue.put(self.state)

    def on(self):
        self.state = "red_on"
        self.queue.put(self.state)

    def on_green(self):
        self.on()

    def off_green(self):
        self.off()

    def renew(self):
        while True:
            sleep(3)
            self.queue.put(self.state)

    def _consume(self):
        while True:
            while not self.queue.empty():
                value = self.queue.get()
                self.nodemcu.send(value)
                self.queue.task_done()
            sleep(0.05)