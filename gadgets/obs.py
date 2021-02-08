import threading

from obswebsocket import obsws, requests, events
from time import sleep
import logging
import win32api
import win32gui
import win32con


# logging.basicConfig(level=logging.DEBUG)


class Obs:
    def __init__(self, window_name):
        self.window_name = window_name
        self.ws = obsws("localhost", 4444, "secret")
        self.ws.connect()

    def _send_key(self, key):
        hwndMain = win32gui.FindWindow(None, self.window_name)
        hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
        win32api.PostMessage(hwndChild, win32con.WM_CHAR, key, 0)

    def zoom_cams_in(self):
        self._send_key(0x74)

    def zoom_cams_out(self):
        self._send_key(0x75)

    def show_projector(self):
        self._send_key(0x76)

    def hide_projector(self):
        self._send_key(0x77)

    def _call(self, obj):
        return self.ws.call(obj)

    def _switch_scene(self, name):
        curr = self._call(requests.GetCurrentScene()).datain["name"]
        if curr == name:
            return
        self._call(requests.SetCurrentScene(name))

    def switch_to_sing(self):
        self._switch_scene("split")

    def switch_to_default(self):
        self._switch_scene("default")

    def show_donate(self):
        self._send_key(0x79)

    def hide_donate(self):
        self._send_key(0x78)

    def show_source(self, name):
        self._call(requests.SetSceneItemProperties(name, visible=True))

    def hide_source(self, name):
        self._call(requests.SetSceneItemProperties(name, visible=False))

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
    obs.show_source("sub_icon")
    while True:
        sleep(1)
