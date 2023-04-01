import os
from threading import Thread

from PIL import Image

from buttons.button import ButtonBase
from gadgets.obs import Obs
from time import time, sleep
from utils import format_time


class ReplayButton(ButtonBase):

    def __init__(self, obs: Obs):
        super().__init__()
        self.active = False
        self.obs = obs
        self.default_icon = Image.open(os.path.abspath(f"./assets/icons/rec.png"))
        self.image = self.default_icon
        self.start = 0

    def on_press(self):
        if self.active:
            self.image = self.default_icon
            self.obs.stop_replay_buffer()
            self.active = False
        else:
            self.start = time()
            self.image = self.render_text("0:00", "green", 20)
            self.active = True
            self.obs.start_replay_buffer()
            Thread(target=self._update_loop).start()

    def _update_loop(self):
        while self.active:
            sleep(1)
            if not self.active:
                break

            t = time() - self.start
            elapsed = int(t)
            self.image = self.render_text(format_time(elapsed), "green", 20)
