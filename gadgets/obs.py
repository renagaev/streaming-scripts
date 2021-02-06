import threading

from obswebsocket import obsws, requests, events
from time import sleep
import logging
import win32api
import win32gui
import win32con


# logging.basicConfig(level=logging.DEBUG)


class Obs:
    def __init__(self):
        self.ws = obsws("localhost", 4444, "secret")
        self.ws.connect()

    @staticmethod
    def send_key(key):
        name = "OBS 26.0.2 (64-bit, windows) - Profile: Безымянный - Scenes: Безымянный"
        hwndMain = win32gui.FindWindow(None, name)
        hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
        win32api.PostMessage(hwndChild, win32con.WM_CHAR, key, 0)

    def _call(self, obj):
        return self.ws.call(obj)

    def _switch_scene(self, name):
        curr = self._call(requests.GetCurrentScene()).datain["name"]
        if curr == name: return
        self._call(requests.SetCurrentScene(name))

    def switch_to_sing(self):
        self._switch_scene("sing")

    def switch_to_default(self):
        self._switch_scene("default")

    def set_zoom_level(self, value):
        self._call(requests.SetVolume("zoom", value))

    def set_mic_level(self, value):
        self._call(requests.SetVolume("mic", value))

    def transform_to_level(self, source, level):
        current = self._call(requests.GetVolume(source)).datain["volume"]
        step = 1 / 32
        if level < current:
            step *= -1
        while True:
            a = min(level - current, step, key=abs)
            current += a
            self._call(requests.SetVolume(source, current))
            if abs(current - level) < 0.000001:
                break

    def transform_sound(self, mic_level, zoom_level):
        threading.Thread(target=self.transform_to_level, args=("mic", mic_level)).start()
        threading.Thread(target=self.transform_to_level, args=("zoom", zoom_level)).start()

    def scale(self):
        self._call(requests.SetSceneItemTransform("txt", x_scale=0.7, y_scale=0.7, rotation=0))
        self._call(requests.SetSceneItemProperties("txt", position_alignment=3))


if __name__ == '__main__':
    obs = Obs()
    obs.transform_sound(0, 1)
    while True:
        sleep(1)
