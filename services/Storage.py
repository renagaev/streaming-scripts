import sqlite3
from datetime import *
from typing import Iterable


class KeyFrame:
    def __init__(self, created: datetime, stream_started: datetime):
        self.created = created
        self.stream_started = stream_started
        self.elapsed: timedelta = created - stream_started


class Record:
    def __init__(self, created, stream_started, note):
        self.note = note
        self.stream_started = stream_started
        self.creted = created
        self.elapsed: timedelta = created - stream_started


class Storage:
    def create_connection(self):
        return sqlite3.connect("storage.sqlite",
                               detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    def __init__(self):
        with self.create_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS keyframes (
                                    created timestamp,
                                    stream_start timestamp,
                                    note text);""")

    def record_keyframe(self, keyframe: KeyFrame):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("insert into keyframes (created, stream_start) values (?, ?);",
                           (keyframe.created, keyframe.stream_started))
            conn.commit()

    def add_text(self, created, text):
        with self.create_connection() as conn:
            try:
                r = conn.execute("""update keyframes set note = ? where rowid in 
                                (select rowid from keyframes where created < ? order by created desc limit 1);""",
                             (text, created))
            except Exception as e:
                print(e)
            x = 0

    def load_timestamps_on_date(self, creation_date: datetime) -> Iterable[Record]:
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("select created, stream_start, note from keyframes where date(created) = date(?)",
                           [creation_date])
            res = [Record(i[0], i[1], i[2]) for i in cursor.fetchall()]
            return res


if __name__ == '__main__':
    from time import sleep

    storage = Storage()
    now = datetime.now()
    storage.record_keyframe(KeyFrame(now - timedelta(seconds=10), datetime.now() - timedelta(minutes=1, seconds=10)))
    storage.record_keyframe(KeyFrame(now, datetime.now() - timedelta(minutes=1, seconds=10)))
    storage.add_text(datetime.now(), "asssas")
    x = storage.load_timestamps_on_date(datetime.now())
    s = 0
