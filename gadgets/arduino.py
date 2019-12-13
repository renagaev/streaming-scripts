import serial
from threading import Thread
from queue import Queue
from time import sleep

class Arduino:
    def __init__(self, dummy=False):

        self.queue = Queue()
        self._consumer = Thread(target=self._consume)
        if not dummy:
            self._consumer.start()
            self.port = serial.Serial("COM3", 9600)

    def command(self, cam, bright):
        bright = int(bright)
        self.queue.put(f"{cam} {bright};".encode("utf-8"))

    def hard(self, cam):
        for i in range(4):
            self.command(i, 0)
        self.command(cam, 127)

    def on(self, cam):
        self.command(cam, 127)

    def off(self, cam):
        self.command(cam, 0)

    def _consume(self):
        while True:
            while not self.queue.empty():
                string = self.queue.get()
                self.port.write(string)
                self.queue.task_done()
            sleep(0.05)

