import requests
import subprocess
import os
from pywinauto import Application


class Vmix:
    current_zoom = 1
    run_zoom_in = False
    run_zoom_out = False

    def __init__(self):
        path = "C:\Program Files (x86)\\vMix\\vmix64.exe"
        self.url = "http://127.0.0.1:8088/api"
        self.mac = 2
        self.app = Application().connect(path=path)
        self.main_window = self.app.window(title_re=".*Pro.*")

    def enable_input(self, inp=None):
        if inp is None:
            inp = self.mac
        self._call(f"overlayinput{inp}in", input=inp)

    def disable_input(self, inp=None):
        if inp is None:
            inp = self.mac
        self._call(f"overlayinput{inp}out", input=str(inp))

    def set_title_text(self, inp, text):
        self._call("settext", text, str(inp))

    def set_zoom(self, inp, value):
        self._call("setzoom", value=value, input=inp)

    def stop_zoom(self):
        run_zoom_in = False
        run_zoom_out = False

    def start_stream(self):
        self._call("startstreaming")

    def stop_stream(self):
        self._call("stopstreamih")

    def start_recording(self):
        self._call("startrecording")

    def stop_recording(self):
        self._call("stoprecording")

    def load_preset(self):
        self._call("openpreset", "C:\\Users\Admin\Documents\\vMixStorage\church.vmix")

    def start_multicorder(self):
        self._call("startmulticorder")

    def stop_multicorder(self):
        self._call("stopmulticorder")

    def add_video_input(self, path):
        self._call("addinput", path)

    def play_input(self, input):
        pass

    def _call(self, function, value=None, input=None):
        params = {
            "function": function
        }
        if value is not None:
            params["value"] = value
        if input is not None:
            params["input"] = input
        requests.get(self.url, params)

    def set_stream_key(self, key):
        self.main_window.set_focus()
        self.main_window.child_window(auto_id="cmdStreamingSetup", control_type="kzzzzzw").click_input()
        settings_window = self.app["Streaming Settings"]
        settings_window["Edit2"].set_text(key)
        settings_window["Save and CloseButton"].click()

    def open_insight(self):
        if self.app["Insight 2"].exists():
            return
        self.main_window.set_focus()
        self.main_window["MasterButton2"].click_input()
        settings_window = self.app["Audio Settings - Master"]
        settings_window.click_input(coords=(10, 80))
        plugins_list = settings_window.child_window(auto_id="chkPlugins", control_type="vMix.UICheckedListBox")
        insight_index = plugins_list.item_texts().index("Insight 2")
        plugins_list.select(insight_index)
        settings_window["'Show EditorButton"].click_input()
        settings_window.close()
        self.adjust_windows()

    def adjust_windows(self):
        insight = self.app["Insight 2"]
        insight.move_window(x=1470, y=0)
        self.main_window.move_window(width=1488, repaint=True)


if __name__ == '__main__':
    import time

    v = Vmix()
    v.start_multicorder()
    time.sleep(10)
    v.stop_multicorder()
