from buttons.button import ButtonBase
from gadgets.vmix import Vmix
from store import store


class AddTrailerButton(ButtonBase):
    def __init__(self, vmix: Vmix):
        self.vmix = vmix
        super().__init__()

    def on_press(self):
        path = store["trailer"]["path"]
        _len = store["trailer"]["len"]
        if path:
            self.vmix.add_video_input(path)

