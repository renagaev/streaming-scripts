import os
from threading import Timer

from PIL import Image

from buttons.button import ButtonBase
from gadgets.obs import Obs
from gadgets.roland import Roland
from store import store


class SceneSwitchButton(ButtonBase):

    def __init__(self, obs: Obs, roland: Roland):
        super().__init__()
        self.roland = roland
        self.obs = obs
        self.default_icon = Image.open(os.path.abspath(f"./assets/icons/split.png"))
        self.split_icon = Image.open(os.path.abspath(f"./assets/icons/split-enabled.png"))
        self.image = self.default_icon
        self.scene = "default"

    def _icon(self):
        if self.scene == "default":
            return self.default_icon
        return self.split_icon

    def switch_to_first_cam(self):
        fade_len = self.roland.fade_len
        self.roland.set_zero_fade_len()
        self.roland.transform_to_cam(0)
        store.cam.value = 0
        self.roland.set_fade_len(fade_len)

    def on_press(self):

        if self.scene == "default":
            duration = self.obs.get_transition_duration() / 2 / 1000
            Timer(duration, self.switch_to_first_cam).start()
            self.scene = "split"
            self.image = self.split_icon
            self.obs.switch_to_split()
        else:
            self.scene = "default"
            self.image = self.default_icon
            self.obs.switch_to_default()
