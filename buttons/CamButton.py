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
        self.start = None
        self.image = self.render_text(str(self.index + 1), "black", 20)
        store.cam.subscribe(self._on_cam_change)

    def on_press(self):
        if store.cam.value == self.index:
            return
        store.cam.value = self.index
        self.lamps.on(self.index)
        self.roland.transform_to_cam(self.index)
        self.image = self.render_text("0:00", "green", 20)
        self.start = time()
        Thread(target=self._update_loop).start()

    def _on_cam_change(self, cam_value):
        if cam_value != self.index:
            self.image = self.render_text(str(self.index + 1), "black", 20)


    def _update_loop(self):
        prev = 0
        color = 'green'
        while store.cam.value == self.index:
            sleep(0.2)
            if store.cam.value != self.index:
                break
            t = time() - self.start
            if t // 0.33 == prev:
                continue
            prev = t // 0.33
            elapsed = int(t)
            minutes = str(elapsed // 60)
            seconds = elapsed % 60
            seconds = "0" + str(seconds) if seconds < 10 else seconds
            if elapsed > 60:
                color = 'red' if color == 'green' else 'green'
            text = f"{minutes}:{seconds}"
            self.image = self.render_text(text, color, 20)
        self.lamps.off(self.index)
        #self.image = self.render_text(str(self.index + 1), "black", 20)
