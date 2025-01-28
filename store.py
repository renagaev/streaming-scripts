from threading import Thread


class ReactiveValue:
    def __init__(self, value):
        self._value = value
        self._callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for callback in self._callbacks:
            Thread(target=callback, args=(value,)).start()

    def subscribe(self, callback):
        self._callbacks.append(callback)


class Store:
    def __init__(self):
        self.cam = ReactiveValue(-1)
        self.waiting_cam = ReactiveValue(-1)
        self.words_showed = ReactiveValue(False)
        self.aten_cam = ReactiveValue(4)


store = Store()
