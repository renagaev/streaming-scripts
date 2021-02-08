from buttons.button import ButtonBase
from gadgets.obs import Obs


class WordsButton(ButtonBase):

    def __init__(self, obs: Obs):
        super().__init__()
        self.obs = obs
        self.on = False
        self.image = self._icon()

    def _icon(self):
        if self.on:
            return self.render_icon("align-left", "green")
        return self.render_icon("align-left")

    def on_press(self):
        self.on = not self.on
        print(f"on = {self.on}")
        if self.on:
            Obs.send_key(0x76)
        else:
            Obs.send_key(0x77)
        self.image = self._icon()
