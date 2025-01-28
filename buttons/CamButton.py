from threading import Thread, Timer

from Lamps.LampsSwitch import LampsSwitch
from buttons.button import ButtonBase
from store import store
from time import time, sleep
from utils import format_time


class CamButton(ButtonBase):

    def __init__(self, roland, lamps: LampsSwitch, index):
        super().__init__()
        self.lamps: LampsSwitch = lamps
        self.index = index
        self.roland = roland
        self.start = None
        self.image = self.render_text(str(self.index + 1), "black", 20)
        self.waiting = False
        self.timer = None
        store.cam.subscribe(self._on_cam_change)
        store.waiting_cam.subscribe(self._on_waiting_cam_change)

    def enable(self):
        self.lamps.on(self.index)
        self.roland.transform_to_cam(self.index)
        self.image = self.render_text("0:00", "green", 20)
        self.start = time()
        Thread(target=self._update_loop).start()

    def on_press(self):
        if self.waiting:
            self.transition_to_cam()
            if self.timer:
                self.timer.cancel()
        else:
            store.waiting_cam.value = self.index
            self.waiting = True
            self.timer = Timer(2, self.transition_to_cam)
            self.timer.start()
            self.image = self.render_text(str(self.index + 1), "greenyellow", 20)
            self.lamps.on_green(self.index)

    def transition_to_cam(self):
        if not self.waiting or store.waiting_cam.value != self.index:
            return
        if store.cam.value == self.index:
            return
        store.cam.value = self.index
        if store.waiting_cam.value == self.index:
            store.waiting_cam.value = -1
        self.waiting = False
        self.timer.cancel()
        self.timer = None
        self.lamps.off_green(self.index)
        self.enable()

    def _on_cam_change(self, cam_value):
        if cam_value != self.index and not self.waiting:
            self.image = self.render_text(str(self.index + 1), "black", 20)
        else:
            self.enable()

    def _on_waiting_cam_change(self, cam_value):
        if self.waiting and self.index != cam_value:
            self.waiting = False
            if self.timer:
                self.timer.cancel()
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
            if elapsed > 60:
                color = 'red' if color == 'green' else 'green'
            self.image = self.render_text(format_time(elapsed), color, 20)
        self.lamps.off(self.index, delay=self.roland.fade_len)
