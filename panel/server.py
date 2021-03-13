from youtube_dl import YoutubeDL
from flask import Flask

app = Flask(__name__)
youtube = YoutubeDL({'format': 'bestvideo+bestaudio/best', 'outtmpl': 'video.%(ext)s', 'quiet': True})


@app.route("/download")
def download_video(path):
    with youtube:
        res = youtube.download(["-"])
        if res == 0:
            return "ok"
        return "fail"
