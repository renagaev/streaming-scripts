from buttons.button import ButtonBase
from gadgets.vmix import Vmix
from store import store
from time import sleep
from threading import Thread


class ZoomOutButton(ButtonBase):

    def __init__(self, vmix: Vmix):
        super().__init__()
        self.vmix = vmix
        self.data = store["zoom"]
        self.image = self._icon()

    def _icon(self):
        if self.data["out"]:
            if self.data["value"] <= 1:
                return self.render_icon("search-minus", "red")
            return self.render_icon("search-minus", "green")
        return self.render_icon("search-minus", "black")

    def on_press(self):
        if self.data["out"]:
            self.data["out"] = False
        else:
            self.data["out"] = True
            self.data["in"] = False
            Thread(target=self._timer).start()
        self.image = self._icon()

    def _timer(self):
        steps = 300
        time = 10
        z = 0.2
        one_step_time = time / steps
        one_step = z / steps
        target_zoom = 1
        steps = int(abs(target_zoom - self.data["value"]) // one_step)
        for _ in range(steps + 1):
            self.data["value"] -= one_step
            self.vmix.set_zoom(1, self.data["value"])
            if not self.data["out"]:
                break
            sleep(one_step_time)
        self.data["value"] = 1
        self.image = self._icon()
        Thread(target=self._wait_for_change).start()

    def _wait_for_change(self):
        current = self.data["out"]
        while True:
            if self.data["out"] != current:
                self.image = self._icon()
                break
            sleep(0.05)
