import arcade

from globals import get_game, SCREEN_HEIGHT
from label import Label

PADDING = 10
BORDER = 2
WIDTH = 300
WIN_BUDGET = 1000000
LOSE_BUDGET = -300000


class BudgetUI:

    def __init__(self):
        self._negative_budget_bgcolor = arcade.color.RED
        self._budget = 0

        self._value_label = Label('$', 0, 0, font_size=18)
        self._bar_h = self._value_label.get_size()[1] + PADDING
        self._bar_y = SCREEN_HEIGHT - PADDING - self._bar_h

        self._value_label.y = self._bar_y + self._bar_h / 2 - self._value_label.get_size()[1] / 2
        self._value_label.x = PADDING + WIDTH - self._value_label.get_size()[0] - PADDING / 2 - BORDER

    def get_y(self):
        return self._bar_y

    def toggle_negative_budget_bgcolor(self):
        if self._negative_budget_bgcolor == arcade.color.RED:
            self._negative_budget_bgcolor = arcade.color.DARK_RED
        else:
            self._negative_budget_bgcolor = arcade.color.RED

    def update(self, value, text):
        self._budget = value
        self._value_label.text = text
        self._value_label.x = PADDING + WIDTH - self._value_label.get_size()[0] - PADDING / 2 - BORDER

    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(PADDING, self._bar_y, WIDTH, self._bar_h, arcade.color.WHITE)
        arcade.draw_xywh_rectangle_filled(PADDING + BORDER, self._bar_y + BORDER, WIDTH - BORDER * 2,
                                          self._bar_h - BORDER * 2, arcade.color.BLACK)

        if self._budget > 0:
            positive_w = WIDTH - BORDER * 2
            positive_w *= (self._budget / WIN_BUDGET)
            arcade.draw_xywh_rectangle_filled(PADDING + BORDER, self._bar_y + BORDER, positive_w,
                                              self._bar_h - BORDER * 2, arcade.color.GREEN)

        if self._budget < 0:
            arcade.draw_xywh_rectangle_filled(PADDING + BORDER, self._bar_y + BORDER, WIDTH - BORDER * 2,
                                              self._bar_h - BORDER * 2, self._negative_budget_bgcolor)

        self._value_label.on_draw()


class Budget:

    def __init__(self):
        self._budget = 750000
        self._total_time = 0
        self._ui = BudgetUI()

        get_game().register('on_update', self.on_update)
        get_game().register('on_draw', self.on_draw)

    @property
    def ui(self):
        return self._ui

    @staticmethod
    def _budget_as_str_abs(budget):
        if budget < 1000:
            return '${}'.format(budget)
        if budget < 1000000:
            return '${}K'.format(str(budget)[:-3])
        if budget < 1000000000:
            return '${}M'.format(str(budget)[:-6])

    def _budget_as_str(self):
        if self._budget >= 0:
            return Budget._budget_as_str_abs(self._budget)
        return '-' + Budget._budget_as_str_abs(-self._budget)

    def _add_amount(self, amount):
        self._budget += amount
        if self._budget >= WIN_BUDGET:
            self._budget = WIN_BUDGET
            get_game().player_won()
        self._ui.update(self._budget, self._budget_as_str())

    def add_amount(self, amount):
        self._add_amount(amount)

    def lose_amount(self, amount):
        self._add_amount(-amount)

    def on_update(self, dt: float):
        self._total_time += dt
        if self._total_time >= 0.5:
            self._ui.toggle_negative_budget_bgcolor()

            if self._budget < 0:
                self._total_time = 0

    def on_draw(self):
        self._ui.on_draw()
