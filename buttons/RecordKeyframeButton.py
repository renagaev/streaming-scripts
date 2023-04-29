import os

from PIL import Image

from buttons.button import ButtonBase
from gadgets.obs import Obs
from services.Client import Client
from services.Storage import Storage, KeyFrame
from datetime import datetime, timedelta


class RecordKeyframeButton(ButtonBase):
    def __init__(self, client: Client, obs: Obs):
        super().__init__()
        self.obs = obs
        self.client = client
        self.image = Image.open(os.path.abspath(f"./assets/icons/keyframe.png"))

    def on_press(self):
        timecode = self.obs.get_steam_timecode()
        if not timecode:
            return
        now = datetime.now()
        keyframe = KeyFrame(now, now - timecode)
        self.client.record_keyframe(keyframe)
