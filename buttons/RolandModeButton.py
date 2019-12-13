from button import ButtonBase


class RolandModeButton(ButtonBase):

    def __init__(self, roland):
        super().__init__()
        self.roland = roland
        self.mode = "mic"
        self.image = self._icon()

    def _icon(self):
        if self.mode == "cut":
            return self.render_icon("rabbit-fast")
        else:
            return self.render_icon("turtle")

    def on_press(self, deck):
        if self.mode == "mic":
            self.mode = "cut"
        else:
            self.mode = "mic"
        self.roland.mode = self.mode
        self.image = self._icon()
