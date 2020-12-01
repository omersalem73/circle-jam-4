import typing

from globals import get_game, SCREEN_WIDTH, SCREEN_HEIGHT
from label import Label
from random import random

from question_data import QuestionDifficulty, QuestionData


class AudienceShare:

    START_SHARE = 10

    def __init__(self):
        self._share = type(self).START_SHARE
        self._label = Label('', 0, 0)
        self.update()
        get_game().register('on_draw', self.on_draw)

    def _calc_share(self, question_difficulty: QuestionDifficulty):
        probable_change, possible_shift = {
            QuestionDifficulty.EASY: (10, 5),
            QuestionDifficulty.AVERAGE: (20, 5),
            QuestionDifficulty.HARD: (30, 20)
        }[question_difficulty]
        self._share += (random() * probable_change) - possible_shift

        if self._share > 100:
            self._share = 100

    def _share_as_str(self):
        as_str = str(self._share)
        # if as_str[1] == '.':
        #     return as_str[:4] + '%'
        return as_str[:5] + '%'

    def update(self, question_answered: typing.Optional[QuestionData] = None):
        if question_answered is None:
            self._share = type(self).START_SHARE
        else:
            self._calc_share(question_answered.difficulty)
        self._label.text = 'Audience Share: {}'.format(self._share_as_str())
        w, h = self._label.get_size()
        self._label.x = 10
        self._label.y = SCREEN_HEIGHT - 80
        get_game().budget.update()

    def on_draw(self):
        self._label.on_draw()
