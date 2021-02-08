from threading import Thread
from time import sleep
from buttons.button import ButtonBase
from store import store


class BlinkButton(ButtonBase):
    def __init__(self, lamps, index):
        super().__init__()
        self.lamps = lamps
        self.index = index
        self.on = False
        self._on_img = self.render_text(str(self.index + 1), "green", 20)
        self._off_img = self.render_text(str(self.index + 1), "black", 20)
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
            self.lamps.on(self.index)
            sleep(sleep_time)
            self.image = self._off_img
            self.lamps.off(self.index)
            sleep(sleep_time)
        self.lamps.set_state(self.index, store.cam.value == self.index)
