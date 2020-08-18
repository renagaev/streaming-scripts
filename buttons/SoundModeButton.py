from buttons.button import ButtonBase
from gadgets.obs import Obs


class SoundModeButton(ButtonBase):

    def __init__(self, obs: Obs):
        super().__init__()
        self.obs = obs

        self.mode = "mic"
        self.image = self._icon()

    def _icon(self):
        if self.mode == "mic":
            return self.render_icon("microphone")
        else:
            return self.render_icon("volume-up")

    def on_press(self):
        if self.mode == "mic":
            self.mode = "zoom"
        else:
            self.mode = "mic"

        self.obs.change_sound_input(2, self.mode)
        self.image = self._icon()
