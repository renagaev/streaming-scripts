from abc import ABC, abstractmethod


class Lamp(ABC):
    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass

    def set_state(self, on):
        if on:
            self.on()
        else:
            self.off()
