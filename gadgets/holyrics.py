import requests
import re


class Holyrics:

    def __init__(self, url, token):
        self.token = token
        self.url = url

    def __request(self, action, params={}):
        try:
            res = requests.post(f"{self.url}/api/{action}",
                                params={"token": self.token},
                                json=params,
                                headers={'Content-Type': 'application/json'})
            return res.json()["data"]
        except Exception as e:
            return None

    def get_current_song_title(self):
        res = self.__request("GetCurrentPresentation")
        if res is None:
            return None
        if res["type"] != "song":
            return None

        name = res["name"]
        return re.sub("[\d\(\)«»]*", "", name).strip()

    def get_song_title(self, song_id):
        res = self.__request("GetLyrics", {"id": song_id})
        x = 0


if __name__ == '__main__':
    url = "http://192.168.1.107:8092"
    ho = Holyrics(url, "K3XjOv1FsKHXW6g6")
    ho.get_current_song_title()
