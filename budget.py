import arcade

from globals import get_game, SCREEN_HEIGHT, add_timer
from label import Label

PADDING = 10
BORDER = 2
WIDTH = 300
STARTING_BUDGET = 750000
WIN_BUDGET = 1000000
LOSE_BUDGET = -300000
GREEN = (0, 150, 0)
BRIGHT_GREEN = (0, 255, 0)


class BudgetUI:

    def __init__(self):
        self._positive_budget_bgcolor = GREEN
        self._negative_budget_bgcolor = arcade.color.RED
        self._budget = 0

        self._diff_label = Label('+$0', 0, 0, font_size=18)
        self._is_diff_label_visible = False
        self._value_label = Label('$', 0, 0, font_size=18)
        self._bar_h = self._value_label.get_size()[1] + PADDING
        self._bar_y = SCREEN_HEIGHT - PADDING - self._bar_h

        self._value_label.y = self._bar_y + self._bar_h / 2 - self._value_label.get_size()[1] / 2
        self._value_label.x = PADDING + WIDTH - self._value_label.get_size()[0] - PADDING / 2 - BORDER
        self._diff_label.x = PADDING + WIDTH + PADDING
        self._diff_label.y = self._value_label.y

        self._diff_label_timer = None

    def get_y(self):
        return self._bar_y

    def toggle_negative_budget_bgcolor(self):
        if self._negative_budget_bgcolor == arcade.color.RED:
            self._negative_budget_bgcolor = arcade.color.DARK_RED
        else:
            self._negative_budget_bgcolor = arcade.color.RED

    def toggle_positive_budget_bgcolor(self):
        if self._positive_budget_bgcolor == GREEN:
            self._positive_budget_bgcolor = BRIGHT_GREEN
        else:
            self._positive_budget_bgcolor = GREEN

    def _hide_diff_label(self):
        self._is_diff_label_visible = False
        self._diff_label_timer = None

    def update(self, value, text, diff_value, diff_text):
        self._budget = value
        self._value_label.text = text
        self._value_label.x = PADDING + WIDTH - self._value_label.get_size()[0] - PADDING / 2 - BORDER
        self._positive_budget_bgcolor = GREEN

        if diff_value < 0:
            self._diff_label.color = arcade.color.RED
        elif diff_value > 0:
            self._diff_label.color = arcade.color.GREEN
            diff_text = '+{}'.format(diff_text)
        else:
            self._is_diff_label_visible = False
            return

        self._is_diff_label_visible = True
        self._diff_label.text = diff_text

        if self._diff_label_timer is None:
            self._diff_label_timer = add_timer(2, lambda: self._hide_diff_label())
        else:
            self._diff_label_timer.reset_seconds(2)

    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(PADDING, self._bar_y, WIDTH, self._bar_h, arcade.color.WHITE)
        arcade.draw_xywh_rectangle_filled(PADDING + BORDER, self._bar_y + BORDER, WIDTH - BORDER * 2,
                                          self._bar_h - BORDER * 2, arcade.color.BLACK)

        if self._budget > 0:
            positive_w = WIDTH - BORDER * 2
            positive_w *= (self._budget / WIN_BUDGET)
            arcade.draw_xywh_rectangle_filled(PADDING + BORDER, self._bar_y + BORDER, positive_w,
                                              self._bar_h - BORDER * 2, self._positive_budget_bgcolor)

        if self._budget < 0:
            arcade.draw_xywh_rectangle_filled(PADDING + BORDER, self._bar_y + BORDER, WIDTH - BORDER * 2,
                                              self._bar_h - BORDER * 2, self._negative_budget_bgcolor)

        self._value_label.on_draw()

        if self._is_diff_label_visible:
            self._diff_label.on_draw()


class Budget:

    def __init__(self):
        self._budget = STARTING_BUDGET
        self._total_time = 0
        self._ui = BudgetUI()

        get_game().register('on_update', self.on_update)
        get_game().register('on_draw', self.on_draw)

        self.add_amount(0)

    def get(self):
        return self._budget

    def reset(self):
        self._budget = STARTING_BUDGET
        self._ui.update(self._budget, self._budget_as_str(self._budget), 0, '')

    @property
    def ui(self):
        return self._ui

    @staticmethod
    def _abs_budget_as_str_abs(budget):
        if budget < 1000:
            return '${}'.format(budget)
        if budget < 1000000:
            return '${}K'.format(str(budget)[:-3])
        if budget < 1000000000:
            return '${}M'.format(str(budget)[:-6])

    @staticmethod
    def _budget_as_str(budget):
        if budget >= 0:
            return Budget._abs_budget_as_str_abs(budget)
        return '-' + Budget._abs_budget_as_str_abs(-budget)

    def _add_amount(self, amount):
        self._budget += amount
        if self._budget >= WIN_BUDGET:
            amount = WIN_BUDGET - (self._budget - amount)
            self._budget = WIN_BUDGET
        elif self._budget <= LOSE_BUDGET:
            amount = LOSE_BUDGET - (self._budget - amount)
            self._budget = LOSE_BUDGET
        self._ui.update(self._budget, self._budget_as_str(self._budget), amount, self._budget_as_str(amount))

    def add_amount(self, amount):
        self._add_amount(amount)

    def lose_amount(self, amount):
        self._add_amount(-amount)

    def on_update(self, dt: float):
        self._total_time += dt
        if self._total_time >= 0.5:
            self._total_time = 0
            if self._budget < 0:
                self._ui.toggle_negative_budget_bgcolor()
            elif self._budget == WIN_BUDGET:
                self._ui.toggle_positive_budget_bgcolor()

    def on_draw(self):
        self._ui.on_draw()
