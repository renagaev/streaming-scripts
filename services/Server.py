from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from services.Storage import Storage, Record
from flask_socketio import SocketIO, emit


class Endpoints:
    def __init__(self, storage: Storage, socketio):
        self.socketio = socketio
        self.storage = storage

    def get_formatted_keyframes(self):
        keyframes = self.storage.get_last_keyframes()
        lst = []
        for idx, item in enumerate(keyframes):
            item: Record = item
            txt = item.id
            if item.note:
                txt = item.note
            elif item.candidates:
                txt = item.candidates[-1]

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
        record = self.storage.record_keyframe(created, stream_started)
        self.socketio.emit("new-keyframe", self.to_dict(record))
        return "ok"

    def set_text(self):
        res = self.storage.record_text(datetime.now(), request.args["text"])
        if res is not None:
            id, text = res
            self.socketio.emit("new-candidate", data=(id, text))
        return "ok"


def run_app(storage: Storage):
    app = Flask(__name__)
    CORS(app)
    socketio = SocketIO()
    socketio.init_app(app, cors_allowed_origins="*")

    endpoints = Endpoints(storage, socketio)
    app.add_url_rule("/formatted-keyframes", view_func=endpoints.get_formatted_keyframes)
    app.add_url_rule("/keyframes", view_func=endpoints.get_keyframes)
    app.add_url_rule("/keyframe", view_func=endpoints.record_keyframe, methods=["POST"])
    app.add_url_rule("/text", view_func=endpoints.set_text, methods=["POST"])
    app.add_url_rule("/update-note", view_func=endpoints.update_note, methods=["POST"])

    socketio.run(app, "localhost", 8080, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    run_app(Storage())
