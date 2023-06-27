import threading
import time
from time import sleep

from obswebsocket import obsws, requests
from datetime import datetime, timedelta


# logging.basicConfig(level=logging.DEBUG)


class Obs:
    def __init__(self):
        self.ws = obsws("localhost", 4454, "secret" )
        self.a = datetime.now()
        self.ws.connect()

    def set_file(self, source, path):
        self._call(requests.SetSourceSettings(source, {"local_file": path}))

    def get_steam_timecode(self):
        res = self._call(requests.GetStreamStatus())
        if res.getOutputActive():
            dt = datetime.strptime(res.getOutputTimecode(), "%H:%M:%S.%f")
            return timedelta(seconds=dt.hour * 3600 + dt.minute * 60 + dt.second)

    def _hotkey(self, name):
        self._call(requests.TriggerHotkeyByName(hotkeyName=name))

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

    def recreate_projector(self):
        self._hotkey("recreate-projector")

    def start_replay_buffer(self):
        self._call(requests.StartReplayBuffer())

    def stop_replay_buffer(self):
        self._call(requests.SaveReplayBuffer())
        self._call(requests.StopReplayBuffer())

    def get_transition_duration(self):
        res = self._call(requests.GetCurrentSceneTransition())
        return res.getTransitionDuration()

    def is_streaming(self):
        return self._call(requests.GetStreamingStatus()).datain["recording"]

    def end_stream_and_recording(self):
        self._call(requests.StopRecording())
        self._call(requests.StopStreaming())

    def _call(self, obj):
        return self.ws.call(obj)

    def _switch_scene(self, name):
        curr = self._call(requests.GetCurrentProgramScene()).getCurrentProgramSceneName()
        if curr == name:
            return
        self._call(requests.SetCurrentProgramScene(sceneName=name))

    def switch_to_split(self):
        self._switch_scene("split")

    def switch_to_default(self):
        self._switch_scene("default")

    def show_source(self, name):
        self._call(requests.SetSceneItemProperties(name, visible=True))

    def hide_source(self, name):
        self._call(requests.SetSceneItemProperties(name, visible=False))

    def transform_to_level(self, source, level):
        s = requests.GetVolume()
        current = self._call(requests.GetInputVolume(inputName=source)).getInputVolumeMul()
        step = 1 / 32
        if level < current:
            step *= -1
        while True:
            a = min(level - current, step, key=abs)
            current += a
            self._call(requests.SetInputVolume(inputName=source, inputVolumeMul=current))
            time.sleep(0.05)
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

    settings = {
        'last_video_device_id': 'FHD Capture:\\\\?\\usb#22vid_1bcf&pid_2c99&mi_00#227&28cf3259&0&0000#22{65e8773d-8f56-11d0-a3b9-00a0c9223196}\\global',
        'video_device_id': 'FHD Capture:\\\\?\\usb#22vid_1bcf&pid_2c99&mi_00#227&28cf3259&0&0000#22{65e8773d-8f56-11d0-a3b9-00a0c9223196}\\global'}


    def get_settings():
        obs.ws.call(requests.GetSourceSettings("projector"))


    obs = Obs()
    z = obs.ws.call(requests)
    z = obs.ws.call(requests.GetSourceSettings("sub_icon"))
    z = obs.ws.call(TriggerHotkey("donate-in"))
    r = 0
    while True:
        sleep(1)
