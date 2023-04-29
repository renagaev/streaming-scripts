from flask import Flask, request
from datetime import datetime
from flask_cors import CORS
from services.Storage import Storage, KeyFrame


class Endpoints:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get_today_keyframes(self):
        keyframes = self.storage.load_timestamps_on_date(datetime.now())
        lst = []
        for idx, item in enumerate(keyframes):
            lst.append(f"{str(item.elapsed)} - {item.note if item.note else idx}")
        newline = "\n"
        return f'<pre>{newline.join(lst)}</pre>'

    def record_keyframe(self):
        json = request.json

        keyframe = KeyFrame(created=datetime.fromisoformat(json["created"]),
                            stream_started=datetime.fromisoformat(json["stream_started"]))
        self.storage.record_keyframe(keyframe)
        return "ok"

    def set_text(self):
        self.storage.add_text(datetime.now(), request.args["text"])
        return "ok"


def run_app(storage: Storage):
    app = Flask(__name__)
    # CORS(app)
    endpoints = Endpoints(storage)
    app.add_url_rule("/keyframes", view_func=endpoints.get_today_keyframes)
    app.add_url_rule("/keyframe", view_func=endpoints.record_keyframe, methods=["POST"])
    app.add_url_rule("/text", view_func=endpoints.set_text, methods=["POST"])
    app.run("localhost", 8080, threaded=True)


if __name__ == '__main__':
    run_app(Storage())
