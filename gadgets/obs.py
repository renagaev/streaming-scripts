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

    def _change_sound_input(self, sec=2, to=None):

        steps = 16
        enable = [(i / steps) ** 0.5 * 1 for i in range(steps + 1)]
        disable = enable[::-1]
        zipped = zip(enable, disable) if to == "mic" else zip(disable, enable)
        for e, d in zipped:
            self.set_mic_level(e)
            self.set_zoom_level(d)
            # sleep(step_time)

    def scale(self):
        self._call(requests.SetSceneItemTransform("txt", x_scale=0.7, y_scale=0.7, rotation=0))
        self._call(requests.SetSceneItemProperties("txt", position_alignment=3))

    def change_sound_input(self, sec, to=None):
        thread = threading.Thread(target=self._change_sound_input, args=(sec, to))
        thread.start()


if __name__ == '__main__':
    obs = Obs()
    while True:
        sleep(1)
