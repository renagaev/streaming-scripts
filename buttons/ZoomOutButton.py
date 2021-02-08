from buttons.button import ButtonBase
from gadgets.obs import Obs
from store import store


class ZoomOutButton(ButtonBase):

    def __init__(self):
        super().__init__()
        self.image = self._icon()
        store.zoom.subscribe(self.on_update)

    def _icon(self):
        if store.zoom.value == 0:
            return self.render_icon("search-minus", "red")
        return self.render_icon("search-minus", "black")

    def on_press(self):
        if store.zoom.value == 1:
            store.zoom.value = 0
            Obs.send_key(0x75)

    def on_update(self, zoom_value):
        self.image = self._icon()
