import os

from PIL import Image

from buttons.button import ButtonBase
from gadgets.aten import Aten
from store import store


class AtenSwitchButton(ButtonBase):

    def __init__(self, aten: Aten):
        super().__init__()
        self.aten = aten
        aten.switch(1)
        self.selected = 4
        self.image = self.icon()

    def icon(self):
        i = Image.open(os.path.abspath(f"./assets/icons/4or5_{self.selected}.png"))
        return i

    def on_press(self):
        if self.selected == 4:
            self.aten.switch(2)
            self.selected = 5
            store.aten_cam.value = 5
        else:
            self.aten.switch(1)
            self.selected = 4
            store.aten_cam.value = 4
        self.image = self.icon()
