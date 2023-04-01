import os
from threading import Thread

from PIL import Image

from buttons.button import ButtonBase
from gadgets.obs import Obs
from time import time, sleep
from utils import format_time


class RecreateProjectorButton(ButtonBase):

    def __init__(self, obs: Obs):
        super().__init__()
        self.obs = obs
        self.image = self.render_text("fix\nprojector", "black", 14)

    def on_press(self):
        self.obs.recreate_projector()
