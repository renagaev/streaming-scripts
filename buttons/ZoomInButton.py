import requests

from buttons.button import ButtonBase
from gadgets.obs import Obs
from gadgets.vmix import Vmix
from store import store
from time import sleep
from threading import Thread

class ZoomInButton(ButtonBase):

    def __init__(self):
        super().__init__()
        self.data = store["zoom"]
        self.image = self._icon()

    def _icon(self):
        if self.data["in"]:
            if self.data["value"] >= 1.2:
                return self.render_icon("search-plus", "red")
            return self.render_icon("search-plus", "green")
        return self.render_icon("search-plus", "black")

    def on_press(self):
        if self.data["in"]:
            self.data["in"] = False
        else:
            self.data["in"] = True
            self.data["out"] = False
            Obs.send_key(0x74)
        self.image = self._icon()



    def _timer(self):
        steps = 300
        time = 10
        z = 0.2
        one_step_time = time / steps
        one_step = z / steps
        target_zoom = 1.2
        steps = int(abs(target_zoom - self.data["value"]) // one_step)
        for _ in range(steps+1):
            self.data["value"] += one_step
            self.vmix.set_zoom(1, self.data["value"])
            if not self.data["in"]:
                break
            sleep(one_step_time)
        self.image = self._icon()
        Thread(target=self._wait_for_change).start()

    def _wait_for_change(self):
        current = self.data["in"]
        while True:
            if self.data["in"] != current:
                self.image = self._icon()
                break
            sleep(0.05)




