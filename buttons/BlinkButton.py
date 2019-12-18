from threading import Thread
from time import sleep
from button import ButtonBase

class BlinkButton(ButtonBase):
    def __init__(self, arduino, index):
        super().__init__()
        self.arduino = arduino
        self.index = index
        self.on = False
        self._on_img = self.render_text(str(self.index+1), "green", 20)
        self._off_img = self.render_text(str(self.index+1), "black", 20)
        self.image = self._off_img

    def on_press(self):
        if self.on:
            self.on = False
        else:
            self.on = True
            Thread(target=self._timer).start()

    def _timer(self):
        sleep_time = 0.2
        while self.on:
            self.image = self._on_img
            self.arduino.on(self.index + 1)
            sleep(sleep_time)
            self.image = self._off_img
            self.arduino.off(self.index + 1)
            sleep(sleep_time)
