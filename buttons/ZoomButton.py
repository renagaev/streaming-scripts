from threading import Thread, Timer

from buttons.button import ButtonBase
from gadgets.obs import Obs


class ZoomButton(ButtonBase):

    def __init__(self, obs: Obs):
        super().__init__()
        self.running = False
        self.last = "out"
        self.obs = obs
        self.image = self._icon()

    def _icon(self):

        color = "red" if self.running else "black"
        icon = "search-plus" if self.last == "out" else "search-minus"
        return self.render_icon(icon, color)

    def on_press(self):
        if self.running:
            return
        self.running = True
        self.image = self._icon()
        if self.last == "in":
            self.obs.zoom_cams_out()
        else:
            self.obs.zoom_cams_in()
        Timer(6.0, self.on_end).start()

    def on_end(self):
        self.running = False
        self.last = "in" if self.last == "out" else "out"
        self.image = self._icon()
