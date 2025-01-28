from Lamps.lamp import Lamp
from gadgets.tally import TallySender


class TallyLamp(Lamp):

    def __init__(self, sender: TallySender, port):
        self.pin = port
        self.sender = sender

    def on(self):
        self.sender.set_pin(self.pin, True)

    def off(self):
        self.sender.set_pin(self.pin, False)

    def off_green(self):
        self.sender.set_pin(self.pin - 1, False)

    def on_green(self):
        self.sender.set_pin(self.pin - 1, True)
