from Lamps.lamp import Lamp
from gadgets.arduino import Arduino


class WiredLamp(Lamp):

    def __init__(self, arduino: Arduino, index):
        self.index = index
        self.arduino = arduino

    def on(self):
        self.arduino.on(self.index+1)

    def off(self):
        self.arduino.off(self.index+1)