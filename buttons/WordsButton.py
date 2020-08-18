from buttons.button import ButtonBase
from gadgets.obs import Obs
import requests
import time
class WordsButton(ButtonBase):

    def __init__(self, obs: Obs):
        super().__init__()
        self.obs = obs
        self.on = False
        self.image = self._icon()

    def _icon(self):
        if not self.on:
            return self.render_icon("align-left", "green")
        return self.render_icon("align-left")

    def on_press(self):
        self.on = not self.on
        if self.on:
            print(time.time())
            Obs.send_key(0x77)
        else:
            Obs.send_key(0x76)
        self.image = self._icon()
