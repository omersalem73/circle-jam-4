import arcade

from globals import get_game, sleep_before, SCREEN_WIDTH, SCREEN_HEIGHT
from label import Label
from ui_base import VisibilityToggle


class Stage:
    def __init__(self, money, is_exit_point=False):
        self.money = money
        self.is_exit_point = is_exit_point
        self.color = arcade.color.ORANGE if not is_exit_point else arcade.color.WHITE


STAGES = [Stage(1000), Stage(8000), Stage(16000, True), Stage(32000),
          Stage(125000, True), Stage(500000), Stage(1000000, True)]

SHOW_COST = 70000


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
        return STAGES[self._current_stage_index].is_exit_point

    def get_current_exit_money(self):
        if STAGES[self._current_stage_index].is_exit_point:
            return STAGES[self._current_stage_index].money
        return 0

    def reset_label_colors(self):
        for lbl, stage in zip(self._stages, STAGES):
            lbl.color = stage.color

    def reset(self):
        self.reset_label_colors()
        self._current_stage_index = 0

    def is_current_question_last(self):
        return self._current_stage_index == (len(self._stages) - 1)

    @sleep_before(1)
    def next_stage(self):
        get_game().background_controller.show_select_question()
        self._current_stage_index += 1
        prev_question = get_game().on_screen_question.question_data
        get_game().on_screen_question.reset_data()
        get_game().audience_share.update(prev_question)
        self.show()
        get_game().question_pool.show()

    def draw_if_visible(self):
        if (self._current_stage_index > 0) and (not STAGES[self._current_stage_index - 1].is_exit_point):
            previous_lbl = self._stages[self._current_stage_index - 1]
            previous_lbl.color = arcade.color.ORANGE
        selected_lbl = self._stages[self._current_stage_index]
        if not STAGES[self._current_stage_index].is_exit_point:
            selected_lbl.color = arcade.color.BLACK
        w, h = selected_lbl.get_size()
        arcade.draw_rectangle_filled(selected_lbl.x + self._max_width / 2, selected_lbl.y + h / 2,
                                     self._max_width + self._horizon_padding, h + self._horizon_padding / 4,
                                     arcade.color.ORANGE)
        for lbl in self._stages:
            lbl.on_draw()
