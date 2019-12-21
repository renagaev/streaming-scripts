from buttons.button import ButtonBase
from gadgets.vmix import Vmix


class WordsButton(ButtonBase):

    def __init__(self, vmix: Vmix):
        super().__init__()
        self.vmix = vmix
        self.on = False
        self.image = self._icon()

    def _icon(self):
        if self.on:
            return self.render_icon("align-left", "green")
        return self.render_icon("align-left")

    def on_press(self):
        self.on = not self.on
        if self.on:
            self.vmix.enable_input(2)
        else:
            self.vmix.disable_input(2)
        self.image = self._icon()
