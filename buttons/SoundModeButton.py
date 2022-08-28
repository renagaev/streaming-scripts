from buttons.button import ButtonBase
from gadgets.obs import Obs
from gadgets.roland import Roland


class SoundModeButton(ButtonBase):

    def __init__(self, obs: Obs, roland: Roland):
        super().__init__()
        self.roland = roland
        self.obs = obs

        self.mode = "mic"
        self.image = self._icon()

    def _icon(self):
        if self.mode == "mic":
            return self.render_icon("microphone")
        else:
            return self.render_icon("volume-up")

    def _on_press(self):
        if self.mode == "mic":
            self.mode = "zoom"
        else:
            self.mode = "mic"
        m = "mic" if self.mode == "zoom" else "in"
        self.roland.change_sound_input(2, m)
        self.image = self._icon()

    def on_press(self):
        if self.mode == "mic":
            self.mode = "zoom"
            self.obs.transform_sound(0, 1)
        else:
            self.mode = "mic"
            self.obs.transform_sound(1, 0)
        self.image = self._icon()
