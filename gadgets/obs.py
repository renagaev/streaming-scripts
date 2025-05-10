import json
import threading
import time
from time import sleep

from obswebsocket import obsws, requests
from datetime import datetime, timedelta


# logging.basicConfig(level=logging.DEBUG)


class Obs:
    def __init__(self, rtmp_config_path=None):
        self.ws = obsws("localhost", 4454, "secret")
        self.rtmp_config = rtmp_config_path
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
        return res.getTransitionDuration() or 0

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

    def update_keys(self, vk_key, rutube_key):
        with open(self.rtmp_config, "r", encoding="utf-8-sig") as f:
            config = json.load(f)
        targets = config["targets"]
        vk = [i for i in targets if i["name"] == "vk"][0]
        rutube = [i for i in targets if i["name"] == "rutube"][0]
        vk["service-param"]["key"] = vk_key
        rutube["service-param"]["key"] = rutube_key

        with open(self.rtmp_config, "w", encoding="utf-8-sig") as f:
            json.dump(config, f)

        # переключаем профиль туда-сюда чтоб плагин подхватил изменение конфига
        profiles = self._call(requests.GetProfileList()).datain
        current_profile = profiles["currentProfileName"]
        other_profile = [i for i in profiles["profiles"] if i != current_profile][0]
        self._call(requests.SetCurrentProfile(profileName=other_profile))
        self._call(requests.SetCurrentProfile(profileName=current_profile))


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


    obs = Obs(rtmp_config_path="C:\\Users\\admin\\AppData\\Roaming\\obs-studio\\basic\\profiles\\default\\obs-multi-rtmp.json")
    obs.update_keys("vk 22", "rutube 22")
    d = obs.ws.call(requests.GetOutputList())
    z = obs.ws.call(requests)
    z = obs.ws.call(requests.GetSourceSettings("sub_icon"))
    z = obs.ws.call(TriggerHotkey("donate-in"))
    r = 0
    while True:
        sleep(1)
