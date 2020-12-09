class Timer:

    def __init__(self, seconds, callback):
        self._time_left = seconds
        self._callback = callback
        self._was_called = False

    @property
    def callback(self):
        return self._callback

    @property
    def was_called(self):
        return self._was_called

    def reset_seconds(self, new_seconds):
        self._time_left = new_seconds

    def tick(self, dt):
        self._time_left -= dt
        if self._time_left <= 0:
            self._callback()
            self._was_called = True
