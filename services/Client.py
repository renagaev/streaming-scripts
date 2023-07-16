import datetime

import requests


class Client:

    def __init__(self):
        self.url = "http://127.0.0.1:8080"

    def record_keyframe(self, created, stream_started):
        requests.post(f"{self.url}/keyframe", json={"stream_started": stream_started.isoformat(),
                                                    "created": created.isoformat()})

    def set_text(self, text):
        requests.post(f"{self.url}/text", params={"text": text})

if __name__ == '__main__':
    client = Client()
    now = datetime.datetime.now()
    client.record_keyframe(now, now)
    client.set_text("text3")
    client.set_text("text2")