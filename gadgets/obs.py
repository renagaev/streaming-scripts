import threading
from time import sleep

from obswebsocket import obsws, requests


# logging.basicConfig(level=logging.DEBUG)


class Obs:
    def __init__(self):
        self.ws = obsws("localhost", 4444, "secret")
        self.ws.connect()


    def _hotkey(self, name):
        self._call(TriggerHotkey(name))

    def zoom_cams_in(self):
        self._hotkey("zoom-in")

    def zoom_cams_out(self):
        self._hotkey("zoom-out")

    def show_projector(self):
        self._hotkey("fade-in")

    def hide_projector(self):
        self._hotkey("fade-out")

    def show_donate(self):
        self._hotkey("donate-in")

    def hide_donate(self):
        self._hotkey("donate-out")

    def is_streaming(self):
        return self._call(requests.GetStreamingStatus()).datain["recording"]

    def end_stream_and_recording(self):
        self._call(requests.StopRecording())
        self._call(requests.StopStreaming())



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


class TriggerHotkey(requests.Baserequests):
    def __init__(self, hotkey_name):
        super().__init__()
        self.name = "TriggerHotkeyByName"
        self.dataout["hotkeyName"] = hotkey_name


class TriggerHotkeyBySequence(requests.Baserequests):
    def __init__(self, key_id):
        super().__init__()
        self.datain["keyId"] = key_id
        self.name = "TriggerHotkeyBySequence"


if __name__ == '__main__':
    obs = Obs()
    z = obs.ws.call(requests.GetSourceSettings("sub_icon"))
    z = obs.ws.call(TriggerHotkey("donate-in"))
    r = 0
    while True:
        sleep(1)
