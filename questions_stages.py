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
        self.color = arcade.color.ORANGE if stage_type is StageType.NORMAL else arcade.color.WHITE


STAGES = [Stage(1000), Stage(8000), Stage(16000), Stage(32000, StageType.EXIT_POINT),
          Stage(125000), Stage(500000), Stage(1000000, StageType.EXIT_POINT)]


class QuestionsStages(VisibilityToggle):

    def __init__(self):
        super().__init__()
        self._current_stage_index = 0
        self._stages = []
        for stage in STAGES:
            self._stages.append(Label('${}'.format(stage.money), 0, 0, stage.color))

        self._horizon_padding = 30
        self._max_width = max([lbl.get_size()[0] for lbl in self._stages])
        height_sum = sum([lbl.get_size()[1] for lbl in self._stages]) + (10 * (len(self._stages) - 1))
        current_y = SCREEN_HEIGHT - height_sum - 10
        for i, lbl in enumerate(self._stages):
            lbl.x = SCREEN_WIDTH - self._max_width - self._horizon_padding
            lbl.y = current_y
            current_y += lbl.get_size()[1] + 10
        get_game().register('on_draw', self.on_draw)

    def is_currently_on_exit_point(self):
        return STAGES[self._current_stage_index].stage_type is StageType.EXIT_POINT

    def current_exit_money(self):
        for i in range(self._current_stage_index, -1, -1):
            if STAGES[i].stage_type is StageType.EXIT_POINT:
                return STAGES[i].money
        else:
            return 0

    def reset_label_colors(self):
        for lbl, stage in zip(self._stages, STAGES):
            lbl.color = stage.color

    @sleep_before(2)
    def reset(self):
        get_game().background_controller.show_select_question()
        self.reset_label_colors()
        get_game().budget.lose_amount(self.current_exit_money())
        get_game().contestant_finish_message.show()
        add_timer(2, get_game().contestant_finish_message.hide)

        self._current_stage_index = 0
        get_game().on_screen_question.reset_data()
        get_game().audience_share.update()
        add_timer(0.5, get_game().question_pool.show)
        self.show()

    @sleep_before(2)
    def next_stage(self):
        get_game().background_controller.show_select_question()
        if self._current_stage_index == len(self._stages):
            # TODO: future - choose new contestant?
            self.reset()
        else:
            self._current_stage_index += 1
            prev_question = get_game().on_screen_question.question_data
            get_game().on_screen_question.reset_data()
            get_game().audience_share.update(prev_question)
            if get_game().current_contestant.consider_quitting():
                self.reset()
            self.show()
            add_timer(0.5, get_game().question_pool.show)

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
