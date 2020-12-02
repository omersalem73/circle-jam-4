from globals import get_game, SCREEN_HEIGHT, sleep_before, add_timer
from label import Label
from random import randint

from ui_base import VisibilityToggle


class ContestantFinishMessage(VisibilityToggle):

    def __init__(self):
        super().__init__()
        self._label = Label('Contestant takes home: ${}'.format(0), 10, 0)
        _, h = self._label.get_size()
        self._label.y = SCREEN_HEIGHT - h - 100
        get_game().register('on_draw', self.on_draw)
        self.hide()

    def update(self):
        money = get_game().questions_stages.current_exit_money()
        self._label.text = 'Contestant takes home: ${}'.format(money)

    def draw_if_visible(self):
        self.update()
        self._label.on_draw()
