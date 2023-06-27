import subprocess
from datetime import datetime

from youtube_dl import YoutubeDL
from flask import Flask
import glob
from gadgets.obs import Obs
import random
import os
from threading import Timer


def get_video_duration(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


app = Flask(__name__)
youtube = YoutubeDL({'format': 'bestvideo+bestaudio/best', 'outtmpl': 'video.%(ext)s', 'quiet': True})


class PanelService:
    def __init__(self, obs: Obs, videos_path):
        self.videos_path = videos_path
        self.obs = obs
        self.selected_file = None
        self.file_duration = None
        self.status = "wait"
        self.timer = None

    def select_video(self):
        # if self.obs.is_streaming() or datetime.now().hour > 11:
        #     return

        files = glob.glob(self.videos_path + "/*.mp4")
        file_path = random.choice(files)
        self.file_duration = get_video_duration(file_path)
        self.selected_file = os.path.basename(file_path).replace(".mp4", "")
        self.status = "file_selected"
        self.obs.set_file("start_song", file_path)

        start = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
        to_start = (start - datetime.now()).total_seconds() - self.file_duration
        self.timer = Timer(to_start, self.start)
        self.timer.start()
        


if __name__ == '__main__':
    path = "C:\\Users\\admin\\Documents\\stream_songs"
    s = (datetime.now() - datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)).total_seconds()
    x = datetime.now().weekday()
    s = PanelService(Obs(), path)
    s.select_video()
