from abc import ABC

from buttons.button import ButtonBase
from gadgets.obs import Obs


class ObsButton(ButtonBase, ABC):

    def on_press(self):
        pass

    def init(self):
        while True:
            try:
                return Obs()
            except:
                pass
