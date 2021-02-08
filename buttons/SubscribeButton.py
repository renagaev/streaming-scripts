import random
import time
from threading import Thread

from buttons.button import ButtonBase
from gadgets.obs import Obs
from store import store


class SubscribeButton(ButtonBase):

    def __init__(self, obs: Obs):
        super().__init__()
        self.iterval = 10*60
        self.safe_range = 7
        self.obs = obs
        self.list = [
            "sub_icon",
            "like_sub_notif",
            "notif_square",
            "like_square",
            "like_sub_notif_icon"
        ]
        self.last_name = None
        self.last_time = time.time()
        Thread(target=self.loop).start()

    def get_elapsed(self):
        res = int(self.last_time + self.iterval - time.time())
        if res < 0: return 0
        return res

    def loop(self):
        while True:
            time.sleep(0.3)
            elapsed = self.get_elapsed()
            self.try_show()
            minutes = str(elapsed // 60)
            seconds = elapsed % 60
            seconds = "0" + str(seconds) if seconds < 10 else seconds
            text = f"subs:\n{minutes}:{seconds}"

            color = "black"
            if elapsed <= 7:
                color = "red"
            self.image = self.render_text(text, color, 16)

    def try_show(self):
        if self.get_elapsed() != 0:
            return
        if store.cam.value == 0:
            return
        if store.words_showed.value:
            return
        self.show_random()

    def show_random(self):
        while True:
            name = random.choice(self.list)
            if name != self.last_name:
                break
        self.obs.hide_source(name)
        self.obs.show_source(name)
        self.last_time = time.time()
        self.last_name = name

    def on_press(self):
        if self.get_elapsed() <= self.safe_range:
            self.last_time = time.time()
            return
        self.show_random()
