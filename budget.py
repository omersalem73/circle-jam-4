from globals import get_game, SCREEN_HEIGHT, sleep_before
from label import Label
from random import randint


class Budget:

    def __init__(self):
        self._budget = 100000
        self._label = Label('Budget: {}'.format(self._budget_as_str()), 10, 0)
        _, h = self._label.get_size()
        self._label.y = SCREEN_HEIGHT - h - 10
        self._fast_update()
        get_game().register('on_draw', self.on_draw)

    def _budget_as_str(self):
        return '$' + str(self._budget)

    def _fast_update(self):
        self._budget += randint(-5000, 5000)
        self._label.text = 'Budget: {}'.format(self._budget_as_str())

    @sleep_before(1)
    def update(self):
        self._fast_update()

    def on_draw(self):
        self._label.on_draw()