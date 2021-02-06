import requests

from buttons.button import ButtonBase
from gadgets.obs import Obs
from gadgets.vmix import Vmix
from store import store
from time import sleep
from threading import Thread


class ZoomOutButton(ButtonBase):

    def __init__(self):
        super().__init__()
        self.data = store["zoom"]
        self.state = self.data["value"]
        self.image = self._icon()
        Thread(target=self._wait_for_change).start()

    def _icon(self):
        if self.data["value"] == 0:
            return self.render_icon("search-minus", "red")
        return self.render_icon("search-minus", "black")

    def on_press(self):
        if self.data["value"] == 1:
            self.data["value"] = self.state = 0
            Obs.send_key(0x75)
        self.image = self._icon()

    def _wait_for_change(self):
        while True:
            if self.data["value"] != self.state:
                self.image = self._icon()
            sleep(0.05)
