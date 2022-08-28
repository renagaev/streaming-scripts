import mido
from time import time, sleep
import threading


class Bus:
    def __init__(self, name, cam=None, bright=None):
        self.cam = cam
        self.bright = bright
        self.name = name


a = "a"
b = "b"


class Roland:

    def __init__(self, dummy=False):
        self.dummy = dummy
        self.on_cam_change = lambda x: None
        if not dummy:
            inputs = [i for i in mido.get_input_names() if i.startswith("V-1HD")]
            if len(inputs) == 0:
                print("ROLAND НЕ ПОДКЛЮЧЕН")
            p = mido.get_output_names()
            self.input = mido.open_input(inputs[0])
            outputs = [i for i in mido.get_output_names() if i.startswith("V-1HD")]
            self.input.callback = self.recieve
            self.output = mido.open_output(outputs[0])
        self.a = Bus("a")
        self.b = Bus("b")
        self.selected_bus = None
        self.active_bus = None
        self.last_br = 150
        self.last_transform_time = time()
        self.mode = "cut"
        self.audio = "mic"
        self.noaudio = "in"
        self.muted = False
        self.set_cam(a, 1)
        self.set_cam(b, 1)
        self.transform_to_bus(b)
        self.transform_to_bus(a)
        self.set_mode_to_mix()
        self.fade_len = 0
        # self.change_sound_input(1, self.noaudio)

    def msg(self, *hexs):
        if self.dummy: return
        for hex in hexs:
            msg = mido.Message.from_hex(hex)
            self.output.send(msg)

    def set_cam(self, bus, cam):
        control_msg = f"C0 0{cam}"
        if bus == a:
            self.msg("B0 00 00", "B0 20 00", control_msg)
        else:
            self.msg("B0 00 01", "B0 20 00", control_msg)

    def transform_to_bus(self, bus):
        if bus == a:
            self.msg("B0 14 7F", "B0 14 00")
        else:
            self.msg("B0 15 7F", "B0 15 00")

    def transform_to_cam(self, cam):
        if self.mode == "mix":
            bus = a if self.active_bus == self.b else b
            self.set_cam(bus, cam)
            self.transform_to_bus(bus)
        else:
            bus = b if self.active_bus == self.b else a
            self.set_cam(bus, cam)

    def set_mode_to_mix(self):
        self.msg("B0 13 01")

    def set_long_fade_len(self):
        self.fade_len = 4
        self.msg("B0 12 73")

    def set_shord_fade_len(self):
        self.fade_len = 2
        self.msg("B0 12 1D")

    def set_zero_fade_len(self):
        self.fade_len = 0
        self.msg("B0 12 00")

    def set_fade_len(self, fade_len):
        if fade_len == 4:
            self.set_long_fade_len()
        if fade_len == 2:
            self.set_shord_fade_len()
        if fade_len == 0:
            self.set_zero_fade_len()

    def recieve(self, msg):
        # print(msg, "----", msg.hex())
        if msg.type == "program_change":
            self.selected_bus.cam = msg.program
            if self.selected_bus == self.active_bus:
                self.on_cam_change(self.active_bus.cam)

        elif msg.type == "control_change" and msg.control == 17:
            valid = True

            br = msg.value // 7 * 7
            if br < 20:
                br = 0

            if abs(self.last_br - br) < 10:
                valid = False
            else:
                self.last_br = br

            if msg.value <= 5:
                self.active_bus = self.a
                self.on_cam_change(self.a.cam)

            elif msg.value >= 125:
                self.active_bus = self.b
                self.on_cam_change(self.b.cam)

            if valid:
                self.a.bright = 127 - br
                self.b.bright = br
                for i in [self.a.bright, self.b.bright]:
                    if i < 0:
                        i = 0
                    if i > 127:
                        i = 127
        elif msg.type == "control_change" and msg.control == 0:
            self.selected_bus = self.b if msg.value else self.a

    @staticmethod
    def to_hex(value):
        a = hex(value)[2:]
        return "0" + a if len(a) == 1 else a

    def set_mic_level(self, value):
        if value not in range(128):
            return
        self.msg(f"B0 0F {self.to_hex(value)}")

    def set_audioin_level(self, value):
        if value not in range(128):
            return
        self.msg(f"B0 0E {self.to_hex(value)}")

    def set_audio_level(self, value):
        if self.audio == 'mic':
            self.set_mic_level(value)
        else:
            self.set_audioin_level(value)

    def mute_sound(self):
        self.muted = True
        if self.audio == 'mic':
            s = lambda x: self.set_audioin_level(x)
        else:
            s = lambda x: self.set_mic_level(x)

        sleep_time = 1 / 20
        for i in range(18):
            value = 127 - i / 20 * 127
            value = int(value)
            s(value)
            sleep(sleep_time)
        s(5)

    def unmute_sound(self):
        self.muted = False
        if self.audio == 'mic':
            s = lambda x: self.set_audioin_level(x)
        else:
            s = lambda x: self.set_mic_level(x)

        self.muted = True
        steps = 20
        sleep_time = 1 / 20
        for i in range(20):
            value = i / 20 * 110
            value = int(value)
            s(value)
            sleep(sleep_time)
        s(110)

    def _change_sound_input(self, sec=2, to=None):
        if to is None:
            to = self.noaudio
        elif to == self.audio:
            return
        steps = 15
        step_time = sec / steps

        enable = [int((i / 15) ** 0.5 * 110) for i in range(steps + 1)]
        disable = enable[::-1]
        zipped = zip(enable, disable) if to == "in" else zip(disable, enable)
        for e, d in zipped:
            self.set_mic_level(e)
            self.set_audioin_level(d)
            sleep(step_time)
        self.audio, self.noaudio = self.noaudio, self.audio

    def change_sound_input(self, sec, to=None):
        thread = threading.Thread(target=self._change_sound_input, args=(sec, to))
        thread.start()


if __name__ == '__main__':
    r = Roland("V-1HD 0", "V-1HD 1")
