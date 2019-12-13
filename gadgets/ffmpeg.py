import subprocess
import os
dir_path = "C:\\\\Users\\\\Admin\\\\Documents\\\\vMixStorage\\\\preview\\\\"
ffmpeg_path = "C:\\Users\Admin\Documents\\vMixStorage\python\\ffmpeg.exe"


class Ffmpeg:

    def _call(self, args):
        subprocess.call([ffmpeg_path, *args])

    def concat_videos(self, first, second, output, delete=True):
        with open("temp.txt", "w") as f:
            f.write(f"file {first}\nfile {second}")
        self._call(f"-y -safe 0 -f concat -i temp.txt -c copy {output}".split())
        if delete:
            os.remove(first)
            os.remove(second)
