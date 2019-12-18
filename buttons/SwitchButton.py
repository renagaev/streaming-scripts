from button import ButtonBase
from screen import Screen


class SwitchButton(ButtonBase):

    def __init__(self, deck, screen1: Screen, screen2: Screen):
        super().__init__()
        self.screen0 = screen1
        self.screen1 = screen2
        self.next = 1
        self.deck = deck
        self.image = self.render_text("main", "black", 20)

    def on_press(self):
        if self.next == 1:
            self.screen0.detach()
            self.screen1.attach(self.deck)
            self.next = 0
            self.image = self.render_text("second", "black", 20)
        else:
            self.screen1.detach()
            self.screen0.attach(self.deck)
            self.next = 1
            self.image = self.render_text("main", "black", 20)

