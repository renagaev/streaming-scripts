from StreamDeck.DeviceManager import DeviceManager

from Lamps.LampsSwitch import LampsSwitch
from Lamps.TallyLamp import TallyLamp
from Lamps.WiredLamp import WiredLamp
from Lamps.WirelessLamp import WirelessLamp
from buttons.AtenSwitchButton import AtenSwitchButton
from buttons.DonateButton import DonateButton
from buttons.MixSoundButton import MixSoundButton
from buttons.RecordKeyframeButton import RecordKeyframeButton
from buttons.RecreteProjectorButton import RecreateProjectorButton
from buttons.ReplayButton import ReplayButton
from buttons.SubscribeButton import SubscribeButton
from buttons.SwitchButton import SwitchButton
from buttons.WordsButton import WordsButton
from buttons.ZoomButton import ZoomButton
from buttons.SceneSwitchButton import SceneSwitchButton
from gadgets.arduino import Arduino
from gadgets.aten import Aten
from buttons.MultipleCamButton import MultipleCamButton
from gadgets.holyrics import Holyrics
from gadgets.obs import Obs
from gadgets.tally import TallySender
from screen import Screen
from buttons.CamButton import CamButton
from buttons.BlinkButton import BlinkButton
from buttons.RolandModeButton import RolandModeButton
from buttons.SoundModeButton import SoundModeButton
from buttons.EndStreamButton import EndStreamButton
from gadgets.roland import Roland
from time import sleep

from services.Client import Client
from services.Server import run_app

from services.Storage import Storage
from services.TimeCodeWorker import TimeCodeWorker
from services.yotube import YouTubeScheduler

dummy = False

client = Client()
arduino = Arduino(dummy=True)
tallySender = TallySender()
deck = DeviceManager().enumerate()[0]
roland = Roland(dummy=dummy)
obs = Obs()
aten = Aten(dummy=True)
main_screen = Screen()
second_screen = Screen()
lamps = LampsSwitch()
holyrics = Holyrics("http://192.168.0.115:8094", "IwSRKBWVTWUVe6gu")
youtube = None #YouTubeScheduler("C:\\Users\\admin\PycharmProjects\\streaming-scripts\\secrets\\youtube_secret.json")
timeCodeWorker = TimeCodeWorker(holyrics, client)
names = [
    "Слово. Епископ Рувим Назарчук",
    "Слово. Пастор Евгений Нагаев",
    "Слово. Пастор Олег Гурный",
    "Слово. Диакон Александр Павлов",
    "Слово. Абрам Манукян",
    "Слово. Роберт Тамоян",
    "Слово. Пастор Вячеслав Назарчук",
    "Слово. Пастор Павел Назарчук"
]

lamps.lamps[0] = TallyLamp(tallySender, 3) #WiredLamp(arduino, 0)
lamps.lamps[1] = TallyLamp(tallySender, 5)
lamps.lamps[2] = TallyLamp(tallySender, 7)
lamps.lamps[3] = WiredLamp(arduino, 3)
lamps.lamps[4] = WirelessLamp("192.168.0.144")


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
    zoom_button = ZoomButton(obs)
    scene_switch_button = SceneSwitchButton(obs, roland)
    donate_button = DonateButton(obs)
    subscribe_button = SubscribeButton(obs)
    switch_button = SwitchButton(deck, main_screen, second_screen)
    sound_mix_button = MixSoundButton(obs)
    end_stream_button = EndStreamButton(obs, 30)
    aten_switch_button = AtenSwitchButton(aten)
    replay_button = ReplayButton(obs)
    recreate_projector_button = RecreateProjectorButton(obs)
    keyframe_button = RecordKeyframeButton(client, obs)

    for i in range(4):
        main_screen.buttons[i] = cam_buttons[i]
        second_screen.buttons[i] = cam_buttons[i]
    for i, j in zip(range(4), range(5, 9)):
        main_screen.buttons[j] = blink_buttons[i]
    main_screen.buttons[11] = keyframe_button
    main_screen.buttons[4] = roland_mode_button
    main_screen.buttons[9] = sound_mode_button
    main_screen.buttons[12] = zoom_button
    main_screen.buttons[13] = scene_switch_button
    main_screen.buttons[14] = words_button
    second_screen.buttons[11] = subscribe_button

    second_screen.buttons[13] = sound_mix_button
    second_screen.buttons[11] = donate_button
    second_screen.buttons[12] = recreate_projector_button

    main_screen.buttons[10] = switch_button
    second_screen.buttons[10] = switch_button

    main_screen.attach(deck)


init_streamdeck()
storage = Storage()
timeCodeWorker.run()
run_app(storage, youtube, names)

while True:
    sleep(1)        
