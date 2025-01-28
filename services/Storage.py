import sqlite3
from datetime import datetime, timedelta
from typing import Iterable, List
from tinydb import TinyDB, Query, JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer


class Record:
    def __init__(self, id: int, created: datetime, stream_started: datetime, note: str, candidates: List[str]):
        self.note = note
        self.stream_started = stream_started
        self.created = created
        self.elapsed: timedelta = created - stream_started
        self.candidates = candidates
        self.id = id

    @classmethod
    def from_document(i, document):
        return Record(document.doc_id, document["created"], document["stream_start"], document["text"],
                      document["candidates"])


class Storage:

    def __init__(self):
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(), "TinyDate")
        self.db = TinyDB("db.json", storage=serialization)
        self.keyframes = self.db.table("keyframes")

    def record_keyframe(self, created: str, stream_started, candidates: List[str]):
        keyframe_id = self.keyframes.insert({"created": created,
                                             "stream_start": stream_started,
                                             "text": None,
                                             "candidates": candidates})
        return Record.from_document(self.keyframes.get(doc_id=keyframe_id))

    def record_text(self, created: datetime, text):
        q = Query()
        keyframe = self.keyframes.search(q.created < created)[-1]
        if text not in keyframe["candidates"]:
            keyframe["candidates"].append(text)
            self.keyframes.upsert(keyframe)
            return keyframe.doc_id, text
        return None

    def get_last_keyframes(self) -> Iterable[Record]:
        q = Query()
        last = self.keyframes.all()[-1]
        keyframes = self.keyframes.search(q.stream_start > (last["stream_start"] + timedelta(minutes=-1)))
        return [Record.from_document(i) for i in keyframes]

    def update_note(self, keyframe_id, note):
        keyframe = self.keyframes.get(doc_id=keyframe_id)
        keyframe["text"] = note
        self.keyframes.upsert(keyframe)


if __name__ == '__main__':
    from time import sleep

    storage = Storage()
    now = datetime.now()
    # storage.record_keyframe(now - timedelta(seconds=10), now - timedelta(minutes=1, seconds=10))
    # storage.record_keyframe(now, now - timedelta(minutes=1, seconds=10))
    # storage.record_text(datetime.now(), "asssas")
    x = storage.get_last_keyframes()
    s = 0
