from time import sleep
from threading import Thread
from StreamDeck.ImageHelpers import PILHelper
from queue import Queue
from functools import partial


class Screen:
    def __init__(self):
        self.buttons = [None for _ in range(15)]
        self.deck = None
        self.queue = Queue()
        Thread(target=self._update_loop).start()

    def update_image(self, index, image):
        if self.deck is None or image is None:
            return
        img = PILHelper.to_native_format(self.deck, image)
        args = (index, img)
        self.queue.put(args)

    def on_press(self, deck, key, state):
        if not state:
            return
        if self.buttons[key] is not None:
            Thread(target=self.buttons[key].on_press, args=(deck,)).start()

    def attach(self, deck):
        self.deck = deck
        self.deck.key_callback = self.on_press
        for index, button in enumerate(self.buttons):
            if button is not None:
                self.update_image(index, button.image)
                button.on_image_change = partial(self.update_image, index)

    def detach(self):
        self.deck = None

    def _update_loop(self):
        while True:
            while not self.queue.empty():
                index, image = self.queue.get()
                if self.deck:
                    self.deck.set_key_image(index, image)
                self.queue.task_done()
            sleep(0.05)
