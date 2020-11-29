from globals import get_game, SCREEN_WIDTH, SCREEN_HEIGHT
from label import Label
from random import random


class AudienceShare:

    def __init__(self):
        self._share = 10
        self._label = Label('', 0, 0)
        self.update()
        get_game().register('on_draw', self.on_draw)

    def _calc_share(self):
        self._share += random() * 10 - 5

    def _share_as_str(self):
        as_str = str(self._share)
        if as_str[1] == '.':
            return as_str[:4] + '%'
        return as_str[:5] + '%'

    def update(self):
        self._calc_share()
        self._label.text = 'Audience Share: {}'.format(self._share_as_str())
        w, h = self._label.get_size()
        self._label.x = SCREEN_WIDTH - w - 10
        self._label.y = SCREEN_HEIGHT - h - 10
        get_game().budget.update()

    def on_draw(self):
        self._label.on_draw()
