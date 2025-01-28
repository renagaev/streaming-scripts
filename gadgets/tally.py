from threading import Thread

from pyfirmata import ArduinoNano, util
from time import sleep
import serial.tools.list_ports

class TallySender:
    def __init__(self):
        self.firmata = None
        candidates = [i.device for i in serial.tools.list_ports.comports() if
                      i.description.startswith('USB-SERIAL CH340')]
        for i in candidates:
            self.firmata = ArduinoNano(i, baudrate=57600)
            if self.firmata.get_firmata_version() is not None:
                break

        if self.firmata is None:
            raise Exception("Tally Sender не найден")

        self.it = util.Iterator(self.firmata)
        self.it.start()
        Thread(target=self._loop).start()

    def set_pin(self, number, value):
        self.firmata.digital_ports[0].pins[number].write(value)

    def _loop(self):
        while True:
            self.firmata.digital_ports[0].write()
            sleep(0.05)

if __name__ == '__main__':
    sender = TallySender()

    sender.firmata.digital_ports[1].pins[3].write(True)
    while True:
        try:
            sleep(1)
        except:
            break
