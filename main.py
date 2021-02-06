from StreamDeck.DeviceManager import DeviceManager

from Lamps.LampsSwitch import LampsSwitch
from Lamps.WiredLamp import WiredLamp
from Lamps.WirelessLamp import WirelessLamp
from buttons.DonateButton import DonateButton
from buttons.Init.ObsButton import ObsButton
from buttons.MixSoundButton import MixSoundButton
from buttons.SwitchButton import SwitchButton
from buttons.WordsButton import WordsButton
from buttons.ZoomInButton import ZoomInButton
from buttons.ZoomOutButton import ZoomOutButton
from gadgets.arduino import Arduino
from gadgets.obs import Obs
from screen import Screen
from buttons.CamButton import CamButton
from buttons.BlinkButton import BlinkButton
from buttons.RolandModeButton import RolandModeButton
from buttons.SoundModeButton import SoundModeButton
from gadgets.roland import Roland
from time import sleep

deck = DeviceManager().enumerate()[0]

roland = Roland("V-1HD 0", 'V-1HD 1', dummy=True)
obs = Obs()
arduino = Arduino(dummy=True)
main_screen = Screen()
second_screen = Screen()
lamps = LampsSwitch()

lamps.lamps[0] = WiredLamp(arduino, 0)
lamps.lamps[1] = WirelessLamp("192.168.0.103")
lamps.lamps[2] = WirelessLamp("192.168.0.102")
lamps.lamps[3] = WiredLamp(arduino, 3)

deck.open()
deck.reset()
deck.set_brightness(100)

cam_buttons = [CamButton(roland, lamps, i) for i in range(0, 4)]
blink_buttons = [BlinkButton(lamps, i) for i in range(0, 4)]
roland_mode_button = RolandModeButton(roland)
sound_mode_button = SoundModeButton(obs)
words_button = WordsButton(obs)
zoom_in_button = ZoomInButton()
zoom_out_button = ZoomOutButton()
donate_button = DonateButton()
switch_button = SwitchButton(deck, main_screen, second_screen)
sound_mix_button = MixSoundButton(obs)
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
main_screen.buttons[11] = donate_button
# main_screen.buttons[11] = recording_button
second_screen.buttons[5] = sound_mix_button

main_screen.buttons[10] = switch_button
second_screen.buttons[10] = switch_button

main_screen.attach(deck)

while True:
    sleep(0.1)
