from threading import Thread
from time import sleep

from buttons.button import ButtonBase
from gadgets.obs import Obs
from store import store


class ZoomInButton(ButtonBase):

    def __init__(self):
        super().__init__()
        self.image = self._icon()
        store.zoom.subscribe(self.on_update)

    def _icon(self):
        if store.zoom.value == 1:
            return self.render_icon("search-plus", "red")
        return self.render_icon("search-plus", "black")

    def on_press(self):
        if store.zoom.value == 0:
            store.zoom.value = 1
            Obs.send_key(0x74)

    def on_update(self, zoom_value):
        self.image = self._icon()
