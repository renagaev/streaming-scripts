from threading import Thread

from buttons.button import ButtonBase
from store import store
from time import time, sleep


class CamButton(ButtonBase):

    def __init__(self, roland, lamps, index):
        super().__init__()
        self.lamps = lamps
        self.index = index
        self.roland = roland
        self.data = store["cams"][self.index]
        Thread(target=self._update_loop).start()
        self.image = self.render_text(str(self.index + 1), "black", 20)

    def on_press(self):
        if self.data["on"]:
            return
        for i in store["cams"]:
            i["on"] = False
        self.data["start"] = time()
        self.data["on"] = True

        self.roland.transform_to_cam(self.index)
        self.image = self.render_text("0:00", "green", 20)

    def _update_loop(self):
        on = False
        prev = 0
        color = 'green'
        while True:
            sleep(0.05)
            if self.data["on"]:
                if not on:
                    self.lamps.on(self.index)
                    on = True
                t = time() - self.data["start"]
                if t//0.33 == prev:
                    continue
                prev = t//0.33
                elapsed = int(t)
                minutes = str(elapsed // 60)
                seconds = elapsed % 60
                seconds = "0" + str(seconds) if seconds < 10 else seconds
                if elapsed > 60:
                    color = 'red' if color == 'green' else 'green'
                text = f"{minutes}:{seconds}"
                self.image = self.render_text(text, color, 20)
            else:
                if on:
                    on = False
                    self.lamps.off(self.index)
                if self.image_changed:
                    color = 'green'
                    self.image = self.render_text(str(self.index + 1), "black", 20)
