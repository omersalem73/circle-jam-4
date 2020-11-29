class Timer:

    def __init__(self, seconds, callback):
        self._seconds = seconds
        self._callback = callback
        self._was_called = False

    @property
    def seconds(self):
        return self._seconds

    @property
    def callback(self):
        return self._callback

    @property
    def was_called(self):
        return self._was_called

    def tick(self, dt):
        self._seconds -= dt
        if self._seconds <= 0:
            self._callback()
            self._was_called = True
