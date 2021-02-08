from buttons.button import ButtonBase
from gadgets.obs import Obs
from store import store


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
        store.words_showed.value = self.on
        if self.on:
            self.obs.show_projector()
        else:
            self.obs.hide_projector()
        self.image = self._icon()
