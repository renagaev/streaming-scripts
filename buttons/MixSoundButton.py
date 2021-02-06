from buttons.button import ButtonBase
from gadgets.obs import Obs


class MixSoundButton(ButtonBase):

    def __init__(self, obs: Obs):
        super().__init__()
        self.obs = obs

        self.mode = "mic"
        self.image = self.render_text("sound\nmix", "black", 20)

    def on_press(self):
        self.obs.transform_sound(1, 0.8)
