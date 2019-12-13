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
        x = 0

    def enable_input(self, inp=None):
        if inp is None:
            inp = self.mac
        params = {
            "function": f"overlayinput{inp}in",
            "input": str(inp)
        }
        requests.get(self.url, params)

    def disable_input(self, inp=None):
        if inp is None:
            inp = self.mac
        params = {
            "function": f"overlayinput{inp}out",
            "input": str(inp)
        }
        requests.get(self.url, params)

    def set_title_text(self, inp, text):
        params = {
            "function": "settext",
            "input": str(inp),
            "value": text
        }
        requests.get(self.url, params)

    def set_zoom(self, inp, value):
        params = {
            "function": "setzoom",
            "input": inp,
            "value": value
        }
        requests.get(self.url, params)

    def stop_zoom(self):
        run_zoom_in = False
        run_zoom_out = False

    def start_stream(self):
        params = {
            "function": "startstreaming"
        }
        requests.get(self.url, params)

    def start_recording(self):
        params = {
            "function": "startrecording"
        }
        requests.get(self.url, params)

    def load_preset(self):
        params = {
            "function": "openpreset",
            "value": "C:\\Users\Admin\Documents\\vMixStorage\church.vmix"
        }
        requests.get(self.url, params)
    def start_multicorder(self):
        params = {
            "function": "startmulticorder"
        }
        requests.get(self.url, params)

    def stop_multicorder(self):
        params = {
            "function": "stopmulticorder"
        }
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