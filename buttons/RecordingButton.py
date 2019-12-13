from button import ButtonBase
from gadgets.ffmpeg import Ffmpeg
from gadgets.vmix import Vmix


class RecordingButton(ButtonBase):

    def on_press(self, deck):
        if self.recording:
            return

        self.recording = True
        for i in range(10):
            self.recorded += 1

    def __init__(self, vmix: Vmix, ffmpeg: Ffmpeg):
        super().__init__()
        self.vmix = vmix
        self.ffmpeg = ffmpeg
        self.recording = False
        self.recorded = 0

    def _icon(self):
        