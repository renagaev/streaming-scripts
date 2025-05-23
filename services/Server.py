from typing import List

from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from services.Storage import Storage, Record
from flask_socketio import SocketIO, emit

from services.vk import VkScheduler
from services.yotube import YouTubeScheduler


class Endpoints:
    def __init__(self, storage: Storage, socketio, names: List[str], youtube: YouTubeScheduler):
        self.names = names
        self.youtube = youtube
        self.vk = None
        self.socketio = socketio
        self.storage = storage

    def get_formatted_keyframes(self):
        keyframes = self.storage.get_last_keyframes()
        lst = ["0:00:00 - ?"]
        for idx, item in enumerate(keyframes):
            item: Record = item
            txt = item.id
            if item.note:
                txt = item.note

            lst.append(f"{str(item.elapsed)} - {txt}")
        newline = "\n"
        return f'<pre>{newline.join(lst)}</pre>'

    @staticmethod
    def to_dict(record: Record):
        return {
            "elapsed": str(record.elapsed),
            "note": record.note,
            "candidates": record.candidates,
            "id": record.id
        }

    def get_keyframes(self):
        records = self.storage.get_last_keyframes()
        return jsonify([self.to_dict(i) for i in records])

    def update_note(self):
        id = request.args.get("id")
        note = request.args.get("note")
        self.storage.update_note(id, note)
        return "ok"

    def record_keyframe(self):
        json = request.json

        created = datetime.fromisoformat(json["created"])
        stream_started = datetime.fromisoformat(json["stream_started"])
        record = self.storage.record_keyframe(created, stream_started, self.names)
        self.socketio.emit("new-keyframe", self.to_dict(record))
        return "ok"

    def delete_keyframe(self):
        self.storage.remove_keyframe(int(request.args.get("id")))
        return "ok"

    def set_text(self):
        res = self.storage.record_text(datetime.now(), request.args["text"])
        if res is not None:
            id, text = res
            self.socketio.emit("new-candidate", data=(id, text))
        return "ok"


def run_app(storage: Storage, youtube: YouTubeScheduler, names: List[str]):
    app = Flask(__name__)
    CORS(app)
    socketio = SocketIO()
    socketio.init_app(app, cors_allowed_origins="*")

    endpoints = Endpoints(storage, socketio, names, youtube)
    app.add_url_rule("/formatted-keyframes", view_func=endpoints.get_formatted_keyframes)
    app.add_url_rule("/keyframes", view_func=endpoints.get_keyframes)
    app.add_url_rule("/keyframe", view_func=endpoints.record_keyframe, methods=["POST"])
    app.add_url_rule("/text", view_func=endpoints.set_text, methods=["POST"])
    app.add_url_rule("/update-note", view_func=endpoints.update_note, methods=["POST"])
    app.add_url_rule("/keyframe", view_func=endpoints.delete_keyframe, methods=["DELETE"])

    socketio.run(app, "localhost", 8080, allow_unsafe_werkzeug=True, debug=False)


if __name__ == '__main__':
    access_token = "vk1.a.YApZHGfPBGEvnMLv93MGh_NdJ0IhEE6PdYNDZX68NlJQGWnHqsyheoEiX_aJImbLin8q09AJi6WB8ymVW0U-fOXowbIruu7EFWmYEQ3Ih3Km87KbuZp4Qz9aSVTpRY3XGxkVj5G4PoKR_V9AG1Y0F7QyazWnR8yUis6sm7Nlkkt7dfm7tEJ8ZJAXOzZZwB3H8N0HYnLWJo84O30Hf5fkQQ"
    group_id = "189698294"
    vk = VkScheduler(access_token, group_id)
    youtube = YouTubeScheduler("C:\\Users\\admin\PycharmProjects\\streaming-scripts\\secrets\\youtube_secret.json")
    run_app(Storage(), youtube, vk, [])
