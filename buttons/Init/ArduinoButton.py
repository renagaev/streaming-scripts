from buttons.button import ButtonBase
from gadgets.arduino import Arduino


class ArduinoButton(ButtonBase):
    def on_press(self):
        pass

    def init(self):
        while True:
            try:
                return Arduino(dummy=False)
            except:
                pass
