import requests

from services.Storage import KeyFrame


class Client:

    def __init__(self):
        self.url = "http://127.0.0.1:8080"

    def record_keyframe(self, keyframe: KeyFrame):
        requests.post(f"{self.url}/keyframe", json={"stream_started": keyframe.stream_started.isoformat(),
                                                    "created": keyframe.created.isoformat()})

    def set_text(self, text):
        requests.post(f"{self.url}/text", params={"text": text})
