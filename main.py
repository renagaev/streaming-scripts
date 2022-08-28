from StreamDeck.DeviceManager import DeviceManager

from Lamps.LampsSwitch import LampsSwitch
from Lamps.WiredLamp import WiredLamp
from Lamps.WirelessLamp import WirelessLamp
from buttons.AtenSwitchButton import AtenSwitchButton
from buttons.DonateButton import DonateButton
from buttons.MixSoundButton import MixSoundButton
from buttons.SubscribeButton import SubscribeButton
from buttons.SwitchButton import SwitchButton
from buttons.WordsButton import WordsButton
from buttons.ZoomInButton import ZoomInButton
from buttons.ZoomOutButton import ZoomOutButton
from gadgets.arduino import Arduino
from gadgets.aten import Aten
from buttons.MultipleCamButton import MultipleCamButton
from gadgets.obs import Obs
from screen import Screen
from buttons.CamButton import CamButton
from buttons.BlinkButton import BlinkButton
from buttons.RolandModeButton import RolandModeButton
from buttons.SoundModeButton import SoundModeButton
from buttons.EndStreamButton import EndStreamButton
from gadgets.roland import Roland
from time import sleep

deck = DeviceManager().enumerate()[0]

roland = Roland(dummy=False)
obs = Obs()
arduino = Arduino(dummy=False)
aten = Aten(dummy=False)
main_screen = Screen()
second_screen = Screen()
lamps = LampsSwitch()

lamps.lamps[0] = WiredLamp(arduino, 0)   # WirelessLamp(["192.168.3.141"])
lamps.lamps[1] = WirelessLamp("192.168.0.142") #WirelessLamp("192.168.0.142")
lamps.lamps[2] = WirelessLamp("192.168.0.143") #WirelessLamp("192.168.0.143")
lamps.lamps[3] = WirelessLamp("192.168.0.172")
lamps.lamps[4] = WirelessLamp("192.168.0.169")


def init_streamdeck():
    deck = DeviceManager().enumerate()[0]
    deck.open()
    deck.reset()
    deck.set_brightness(40)

    cam_buttons = [CamButton(roland, lamps, i) for i in range(0, 3)] + [MultipleCamButton(roland, lamps, 3)]
    blink_buttons = [BlinkButton(lamps, i) for i in range(0, 4)]
    roland_mode_button = RolandModeButton(roland)
    sound_mode_button = SoundModeButton(obs, roland)
    words_button = WordsButton(obs)
    zoom_in_button = ZoomInButton(obs)
    zoom_out_button = ZoomOutButton(obs)
    donate_button = DonateButton(obs)
    subscribe_button = SubscribeButton(obs)
    switch_button = SwitchButton(deck, main_screen, second_screen)
    sound_mix_button = MixSoundButton(obs)
    end_stream_button = EndStreamButton(obs, 30)
    aten_switch_button = AtenSwitchButton(aten)

    for i in range(4):
        main_screen.buttons[i] = cam_buttons[i]
        second_screen.buttons[i] = cam_buttons[i]
    for i, j in zip(range(4), range(5, 9)):
        main_screen.buttons[j] = blink_buttons[i]
    main_screen.buttons[11] = aten_switch_button
    main_screen.buttons[4] = roland_mode_button
    main_screen.buttons[9] = sound_mode_button
    main_screen.buttons[12] = zoom_in_button
    main_screen.buttons[13] = zoom_out_button
    main_screen.buttons[14] = words_button
    second_screen.buttons[11] = subscribe_button

    second_screen.buttons[13] = sound_mix_button
    second_screen.buttons[11] = donate_button
    second_screen.buttons[12] = end_stream_button

    main_screen.buttons[10] = switch_button
    second_screen.buttons[10] = switch_button

    main_screen.attach(deck)


init_streamdeck()

while True:
    sleep(1)
