from abc import ABC, abstractmethod


class Lamp(ABC):
    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass

    @abstractmethod
    def on_green(self):
        pass

    @abstractmethod
    def off_green(self):
        pass

    def set_state(self, on):
        if on:
            self.on()
        else:
            self.off()
