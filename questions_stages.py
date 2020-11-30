import arcade

from globals import get_game, sleep_before, add_timer, SCREEN_WIDTH, SCREEN_HEIGHT
from label import Label


class QuestionsStages:

    def __init__(self):
        self._current_stage_index = 0
        self._stages = [Label('${}'.format(10 ** (i + 3)), 0, 0) for i in range(5)]
        self._horizon_padding = 30
        self._max_width = max([lbl.get_size()[0] for lbl in self._stages])
        height_sum = sum([lbl.get_size()[1] for lbl in self._stages]) + (10 * (len(self._stages) - 1))
        current_y = SCREEN_HEIGHT * 0.75 - height_sum / 2
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
        add_timer(0.5, lambda: get_game().question_pool.show())

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
            add_timer(0.5, lambda: get_game().question_pool.show())

    def on_draw(self):
        selected_lbl = self._stages[self._current_stage_index]
        w, h = selected_lbl.get_size()
        arcade.draw_rectangle_filled(selected_lbl.x + self._max_width / 2, selected_lbl.y + h / 2,
                                     self._max_width + self._horizon_padding, h + self._horizon_padding / 4,
                                     arcade.color.ORANGE)
        for lbl in self._stages:
            lbl.on_draw()
