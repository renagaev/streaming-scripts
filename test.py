import mido
import rtmidi
from time import sleep
a = mido.get_output_names()
port = mido.open_output('Microsoft GS Wavetable Synth 0')

for i in range(10):
    msg = mido.Message('control_change', value=i*10, control=11)
    sleep(0.11)
    port.send(msg)
x = 0