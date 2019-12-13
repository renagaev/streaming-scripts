from button import ButtonBase
from gadgets.roland import Roland


class SoundModeButton(ButtonBase):

    def __init__(self, roland: Roland):
        super().__init__()
        self.roland = roland
        self.mode = "mic"
        self.image = self._icon()

    def _icon(self):
        if self.mode == "mic":
            return self.render_icon("microphone")
        else:
            return self.render_icon("volume-up")

    def on_press(self, deck):
        if self.mode == "mic":
            self.mode = "in"
        else:
            self.mode = "mic"

        self.roland.change_sound_input(2, self.mode)
        self.image = self._icon()
