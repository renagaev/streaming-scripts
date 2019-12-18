from button import ButtonBase
from gadgets.ffmpeg import Ffmpeg
from gadgets.vmix import Vmix
from time import sleep
from os.path import join
from os import scandir
from os import remove


class RecordingButton(ButtonBase):

    def __init__(self, vmix: Vmix):
        super().__init__()
        self.vmix = vmix
        self.ffmpeg = Ffmpeg()
        self.recording = False
        self.recorded = 0
        self.base_path = join("C:\\", "Users", "Admin", "Documents", "vMixStorage", "preview")
        self.last = ""
        self.image = self._icon()

    def on_press(self):
        if self.recording:
            return
        self.record()
        self.image = self._icon()
        self.join()

    def record(self):

        self.recording = True
        self.vmix.start_multicorder()
        for i in range(3):
            self.recorded += 1
            self.image = self._icon()
            sleep(1)
        self.vmix.stop_multicorder()
        self.recording = False

    def make_path(self, filename):
        return join(self.base_path, filename).replace("\\", "\\\\")

    def join(self):
        files = list(scandir(self.base_path))
        files = [i for i in files if i.name.endswith("mp4") and i.name != self.last]
        files.sort(key=lambda x: x.stat().st_mtime)
        if not self.last and len(files) < 2:
            return
        if self.last and not files:
            return
        path = lambda x: x.path.replace("\\", "\\\\")
        if not self.last:
            self.ffmpeg.concat_videos(path(files[0]), path(files[1]), self.make_path("1.mp4"))
            self.last = "1.mp4"
        else:
            next_video = self.last.split(".")[0] + "1.mp4"
            self.ffmpeg.concat_videos(path(files[0]), self.make_path(self.last), self.make_path(next_video))
            self.last = next_video
        for file in scandir(self.base_path):
            if file.name != self.last:
                remove(file.path)

    def _icon(self):
        minutes = str(self.recorded // 60)
        seconds = self.recorded % 60
        seconds = "0" + str(seconds) if seconds < 10 else seconds
        text = f"{minutes}:{seconds}"
        if self.recording:
            return self.render_text(text, "green", 20)
        return self.render_text(text, "black", 20)
