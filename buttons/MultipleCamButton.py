from threading import Thread

from buttons.button import ButtonBase
from gadgets.aten import Aten
from store import store
from time import time, sleep
from utils import format_time


class MultipleCamButton(ButtonBase):

    def __init__(self, roland, lamps, index):
        super().__init__()
        self.lamps = lamps
        self.index = index
        self.lamp_index = index
        self.roland = roland
        self.start = None
        self.image = self.render_text(str(self.lamp_index + 1), "black", 20)
        store.cam.subscribe(self._on_cam_change)
        store.aten_cam.subscribe(self._on_aten_cam_change)

    def on_press(self):
        if store.cam.value == self.index:
            return
        store.cam.value = self.index
        self.lamps.on(self.lamp_index)
        m = self.roland.fade_len
        if self.lamp_index == 3 and self.roland.fade_len == 0:
            self.roland.set_shord_fade_len()
        self.roland.transform_to_cam(self.index)
        self.roland.set_fade_len(m)
        self.image = self.render_text("0:00", "green", 20)
        self.lamps.on(self.lamp_index)
        self.start = time()
        Thread(target=self._update_loop).start()

    def _on_aten_cam_change(self, cam_value):
        self.lamps.off(self.lamp_index)
        self.lamp_index = cam_value - 1
        self.image = self.render_text(str(self.lamp_index + 1), "black", 20)

    def _on_cam_change(self, cam_value):
        if cam_value != self.index:
            self.image = self.render_text(str(self.lamp_index + 1), "black", 20)

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
            if elapsed > 60:
                color = 'red' if color == 'green' else 'green'
            self.image = self.render_text(format_time(elapsed), color, 20)
        self.lamps.off(self.lamp_index, delay=self.roland.fade_len)
