from StreamDeck.DeviceManager import DeviceManager

from buttons.RecordingButton import RecordingButton
from buttons.SwitchButton import SwitchButton
from buttons.WordsButton import WordsButton
from buttons.ZoomInButton import ZoomInButton
from buttons.ZoomOutButton import ZoomOutButton
from gadgets.arduino import Arduino
from gadgets.vmix import Vmix
from screen import Screen
from buttons.CamButton import CamButton
from buttons.BlinkButton import BlinkButton
from buttons.RolandModeButton import RolandModeButton
from buttons.SoundModeButton import SoundModeButton
from gadgets.roland import Roland
from time import sleep

deck = DeviceManager().enumerate()[0]
roland = Roland("V-1HD 0", "V-1HD 1", dummy=True)
vmix = Vmix()
arduino = Arduino(dummy=True)
main_screen = Screen()
second_screen = Screen()


deck.open()
deck.reset()
deck.set_brightness(100)


cam_buttons = [CamButton(roland, i) for i in range(0, 4)]
blink_buttons = [BlinkButton(arduino, i) for i in range(0, 4)]
roland_mode_button = RolandModeButton(roland)
sound_mode_button = SoundModeButton(roland)
words_button = WordsButton(vmix)
zoom_in_button = ZoomInButton(vmix)
zoom_out_button = ZoomOutButton(vmix)
recording_button = RecordingButton(vmix)
switch_button = SwitchButton(deck, main_screen, second_screen)

for i in range(4):
    main_screen.buttons[i] = cam_buttons[i]
    second_screen.buttons[i] = cam_buttons[i]
for i, j in zip(range(4), range(5, 9)):
    main_screen.buttons[j] = blink_buttons[i]
main_screen.buttons[4] = roland_mode_button
main_screen.buttons[9] = sound_mode_button
main_screen.buttons[12] = zoom_in_button
main_screen.buttons[13] = zoom_out_button
main_screen.buttons[14] = words_button
main_screen.buttons[11] = recording_button

main_screen.buttons[10] = switch_button
second_screen.buttons[10] = switch_button

main_screen.attach(deck)

while True:
    sleep(0.1)
