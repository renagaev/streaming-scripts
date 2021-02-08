from buttons.button import ButtonBase
from gadgets.obs import Obs


class DonateButton(ButtonBase):
    def __init__(self, obs: Obs):
        super().__init__()
        self.obs = obs
        self.image = self.render_text("donate", "black", 20)
        self.enabled = False

    def on_press(self):
        if self.enabled:
            self.image = self.render_text("donate", "black", 20)
            self.obs.hide_donate()
        else:
            self.image = self.render_text("donate", "green", 20)
            self.obs.show_donate()

        self.enabled = not self.enabled
