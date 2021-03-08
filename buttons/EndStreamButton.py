import time

from buttons.button import ButtonBase
from gadgets.obs import Obs
from utils import format_time
import threading


class EndStreamButton(ButtonBase):

    def __init__(self, obs: Obs, wait_seconds):
        super().__init__()
        self.wait_seconds = wait_seconds
        self.obs = obs
        self.default_image = self.render_text("end\nstream", "black", 19)
        self.image = self.default_image
        self.safe_range = 4
        self.status = None

    def on_press(self):
        if self.status == "wait_confirm":
            if self.obs.is_streaming() or True:
                self.end_stream()
            return
        threading.Thread(target=self.wait_confirm).start()

    def end_stream(self):
        self.obs.transform_sound(0, 0)
        self.obs.hide_source("end_video")
        self.obs.show_source("end_video")
        time.sleep(self.wait_seconds)
        self.obs.end_stream_and_recording()

    def wait_confirm(self):
        self.status = "wait_confirm"
        t = time.time()
        while time.time() - t < self.safe_range:
            time.sleep(0.2)
            if self.status == "ended":
                return
            time_str = format_time(t + self.safe_range - time.time())
            self.image = self.render_text(f"confirm?\n{time_str}", "red", 17)
        self.image = self.default_image
        self.status = None
