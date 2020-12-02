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
          Stage(2000), Stage(4000), Stage(8000), Stage(16000), Stage(32000, StageType.EXIT_POINT),
          Stage(64000), Stage(125000), Stage(500000), Stage(1000000, StageType.EXIT_POINT)]


class QuestionsStages(VisibilityToggle):

    def __init__(self):
        super().__init__()
        self._current_stage_index = 0
        self._current_prize_money = 0
        self._stages = []
        self.reset_label_colors()

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

    def reset_label_colors(self):
        for stage in STAGES:
            color = arcade.color.ORANGE if stage.stage_type is StageType.NORMAL else arcade.color.WHITE
            self._stages.append(Label('${}'.format(stage.money), 0, 0, color))

    @sleep_before(2)
    def reset(self):
        get_game().background_controller.show_select_question()
        self.reset_label_colors()
        get_game().budget.update(self._current_prize_money)
        self._current_stage_index = 0
        self._current_prize_money = 0
        get_game().on_screen_question.reset_data()
        get_game().audience_share.update()
        add_timer(0.5, get_game().question_pool.show)
        self.show()

    @sleep_before(2)
    def next_stage(self):
        get_game().background_controller.show_select_question()
        if self._current_stage_index == len(self._stages):
            # TODO: future - choose new contestant?
            self._current_prize_money = STAGES[-1].money
            self.reset()
        else:
            self._current_stage_index += 1
            if STAGES[self._current_stage_index].stage_type is StageType.EXIT_POINT:
                self._current_prize_money = STAGES[self._current_stage_index].money
            prev_question = get_game().on_screen_question.question_data
            get_game().on_screen_question.reset_data()
            get_game().audience_share.update(prev_question)
            add_timer(0.5, get_game().question_pool.show)
            self.show()

    def draw_if_visible(self):
        if self._current_stage_index > 0 and STAGES[self._current_stage_index - 1].stage_type is StageType.NORMAL:
            previous_lbl = self._stages[self._current_stage_index - 1]
            previous_lbl.color = arcade.color.ORANGE
        selected_lbl = self._stages[self._current_stage_index]
        if STAGES[self._current_stage_index].stage_type is StageType.NORMAL:
            selected_lbl.color = arcade.color.BLACK
        w, h = selected_lbl.get_size()
        arcade.draw_rectangle_filled(selected_lbl.x + self._max_width / 2, selected_lbl.y + h / 2,
                                     self._max_width + self._horizon_padding, h + self._horizon_padding / 4,
                                     arcade.color.ORANGE)
        for lbl in self._stages:
            lbl.on_draw()
