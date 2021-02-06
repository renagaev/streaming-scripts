from buttons.button import ButtonBase
from gadgets.obs import Obs


class DonateButton(ButtonBase):
    def __init__(self):
        super().__init__()
        self.image = self.render_text("donate", "black", 20)
        self.enabled = False

    def on_press(self):
        if self.enabled:
            self.image = self.render_text("donate", "black", 20)
            Obs.send_key(0x78)
        else:
            self.image = self.render_text("donate", "green", 20)
            Obs.send_key(0x79)

        self.enabled = not self.enabled
