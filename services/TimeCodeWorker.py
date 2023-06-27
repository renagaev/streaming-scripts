from threading import Thread

from gadgets.holyrics import Holyrics
from services.Client import Client
import time


class TimeCodeWorker:
    def __init__(self, holyrics: Holyrics, client: Client):
        self.client = client
        self.holyrics = holyrics

    def run(self):
        Thread(target=self.__run).start()

    def __run(self):
        last = None
        while True:
            time.sleep(0.5)
            try:
                curr_song = self.holyrics.get_current_song_title()
                if curr_song is None or curr_song == last:
                    continue

                last = curr_song
                self.client.set_text(f"{last}. Общее пение")

            except Exception as e:
                print(e)
