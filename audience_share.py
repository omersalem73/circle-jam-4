import arcade
import typing

from globals import get_game
from label import Label
from random import random

from question_data import QuestionDifficulty, QuestionData


class AudienceShare:

    START_SHARE = 10

    def __init__(self):
        self._share = type(self).START_SHARE
        self._share_diff_sum = 0
        self._last_share_diff = 0
        self._label = Label('', 0, 0, font_size=20)
        self._diff_label = Label('', 0, 0, font_size=20)
        self.update()
        get_game().register('on_draw', self.on_draw)

    def get_label_y(self):
        return self._label.y

    def _calc_share(self, question_difficulty: QuestionDifficulty):
        stage_coeff = (get_game().questions_stages.current_stage_index + 1)
        if stage_coeff <= 2:
            probable_change, possible_shift = {
                QuestionDifficulty.EASY: (1, 0.25),
                QuestionDifficulty.AVERAGE: (2, 1),
                QuestionDifficulty.HARD: (2, 2)
            }[question_difficulty]
        elif stage_coeff <= 5:
            probable_change, possible_shift = {
                QuestionDifficulty.EASY: (0.5, 0.5),
                QuestionDifficulty.AVERAGE: (1, 0.5),
                QuestionDifficulty.HARD: (2, 1)
            }[question_difficulty]
        else:
            probable_change, possible_shift = {
                QuestionDifficulty.EASY: (2, 2),
                QuestionDifficulty.AVERAGE: (2, 1),
                QuestionDifficulty.HARD: (2, 0)
            }[question_difficulty]

        self._last_share_diff = (random() * probable_change) - possible_shift

        if self._last_share_diff + self._share < 0:
            self._last_share_diff = -self._share

        self._update_diff_lbl(self._last_share_diff)
        self._share += self._last_share_diff
        self._share_diff_sum += self._last_share_diff

        if self._share > 100:
            self._share = 100

    def _update_diff_lbl(self, diff):
        if diff == 0:
            self._diff_label.text = ''
            return

        if diff > 0:
            sign = '+'
            self._diff_label.color = arcade.color.GREEN
        else:
            sign = '-'
            self._diff_label.color = arcade.color.RED

        self._diff_label.text = '({}{})'.format(sign, AudienceShare._share_as_str(diff))

    @staticmethod
    def _share_as_str(share):
        as_str = str(share)
        if as_str[1] == '.':
            return as_str[:4] + '%'
        return as_str[:5] + '%'

    def get_diff_sum(self):
        diff_sum = self._share_diff_sum
        self._share_diff_sum = 0
        sign = '-' if diff_sum < 0 else '+'
        return sign + AudienceShare._share_as_str(diff_sum)

    def reset(self, diff_only=False):
        if diff_only:
            self._last_share_diff = 0
            self._diff_label.text = ''
            return
        self.update()

    def update(self, question_answered: typing.Optional[QuestionData] = None):
        if question_answered is None:
            self._share = type(self).START_SHARE
            self._last_share_diff = 0
            self._diff_label.text = ''
            self._share_diff_sum = 0
        else:
            self._calc_share(question_answered.difficulty)
        self._label.text = 'Rating: {}'.format(AudienceShare._share_as_str(self._share))
        self._label.x = 10
        self._label.y = get_game().budget.ui.get_y() - self._label.get_size()[1] - 5
        self._diff_label.x = self._label.x + self._label.get_size()[0] + 10
        self._diff_label.y = self._label.y

        if self._last_share_diff != 0:
            get_game().budget.add_amount(int(self._last_share_diff * 75000))

    def on_draw(self):
        w_sum = self._label.get_size()[0]
        if len(self._diff_label.text) > 0:
            w_sum += 10 + self._diff_label.get_size()[0]
        arcade.draw_xywh_rectangle_filled(self._label.x - 2, self._label.y - 2, w_sum + 4,
                                          self._label.get_size()[1] + 4, (0, 0, 0, 200))
        self._label.on_draw()
        self._diff_label.on_draw()
