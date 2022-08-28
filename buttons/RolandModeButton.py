import os

from PIL import Image

from buttons.button import ButtonBase


class RolandModeButton(ButtonBase):

    def __init__(self, roland):
        super().__init__()
        self.roland = roland
        self.roland.mode = "mix"
        self.len = 0
        self.roland.set_zero_fade_len()
        self.image = self._icon()

    def _icon(self):
        i = Image.open(os.path.abspath(f"./assets/icons/fade_{self.len}_sec.png"))
        return i


    def on_press(self):
        if self.len == 0:
            self.roland.set_shord_fade_len()
            self.len = 2
        elif self.len == 2:
            self.roland.set_long_fade_len()
            self.len = 4
        else:
            self.roland.set_zero_fade_len()
            self.len = 0
        self.image = self._icon()
