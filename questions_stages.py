from enum import Enum

import arcade

from globals import get_game, sleep_before, add_timer, SCREEN_WIDTH, SCREEN_HEIGHT
from label import Label
from ui_base import VisibilityToggle


class StageType(Enum):
    NORMAL = 'Normal'
    EXIT_POINT = 'Exit Point'


class Stage:
    def __init__(self, money, stage_type=StageType.NORMAL):
        self.money = money
        self.stage_type = stage_type


STAGES = [Stage(100), Stage(200), Stage(500), Stage(1000, StageType.EXIT_POINT),
          Stage(2000), Stage(4000), Stage(8000), Stage(16000, StageType.EXIT_POINT),
          Stage(32000), Stage(64000), Stage(125000, StageType.EXIT_POINT),
          Stage(500000), Stage(1000000, StageType.EXIT_POINT)]


class QuestionsStages(VisibilityToggle):

    def __init__(self):
        super().__init__()
        self._current_stage_index = 0
        self._stages = []
        for stage in STAGES:
            color = arcade.color.ORANGE if stage.stage_type is StageType.NORMAL else arcade.color.WHITE
            self._stages.append(Label('${}'.format(stage.money), 0, 0, color))

        self._horizon_padding = 30
        self._max_width = max([lbl.get_size()[0] for lbl in self._stages])
        height_sum = sum([lbl.get_size()[1] for lbl in self._stages]) + (10 * (len(self._stages) - 1))
        current_y = 100
        for i, lbl in enumerate(self._stages):
            _, h = lbl.get_size()
            lbl.x = SCREEN_WIDTH - self._max_width - self._horizon_padding
            lbl.y = current_y
            current_y += h + 10
        get_game().register('on_draw', self.on_draw)

    @sleep_before(2)
    def reset(self):
        self._current_stage_index = 0
        get_game().on_screen_question.reset_data()
        get_game().audience_share.update()
        add_timer(0.5, get_game().question_pool.show)
        self.show()

    @sleep_before(2)
    def next_stage(self):
        if self._current_stage_index == len(self._stages):
            # TODO: future - choose new contestant?
            self.reset()
        else:
            self._current_stage_index += 1
            prev_question = get_game().on_screen_question.question_data
            get_game().on_screen_question.reset_data()
            get_game().audience_share.update(prev_question)
            add_timer(0.5, get_game().question_pool.show)
            self.show()

    def draw_if_visible(self):
        if self._current_stage_index > 0:
            previous_lbl = self._stages[self._current_stage_index - 1]
            previous_lbl.color = arcade.color.ORANGE
        selected_lbl = self._stages[self._current_stage_index]
        selected_lbl.color = arcade.color.BLACK
        w, h = selected_lbl.get_size()
        arcade.draw_rectangle_filled(selected_lbl.x + self._max_width / 2, selected_lbl.y + h / 2,
                                     self._max_width + self._horizon_padding, h + self._horizon_padding / 4,
                                     arcade.color.ORANGE)
        for lbl in self._stages:
            lbl.on_draw()
