class LampsSwitch:
    def __init__(self):
        self.lamps = [None for _ in range(4)]

    def on(self, index):
        lamp = self.lamps[index]
        if lamp:
            lamp.on()

    def off(self, index):
        lamp = self.lamps[index]
        if lamp:
            lamp.off()

    def set_state(self, index, value):
        lamp = self.lamps[index]
        if lamp:
            lamp.set_state(value)