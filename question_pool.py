import arcade

from globals import SCREEN_WIDTH, SCREEN_HEIGHT, get_game, sleep_before
from ui_base import VisibilityToggle, is_point_in_rect
from label import Label


class QuestionsPool(VisibilityToggle):

    def __init__(self, easy_question, average_question, hard_question):
        super().__init__()
        self._show_highlight = False
        self._highlighted_index = 0
        self._selected_question = None

        easy_question_label = Label(easy_question.text, 0, 0)
        average_question_label = Label(average_question.text, 0, 0)
        hard_question_label = Label(hard_question.text, 0, 0)

        easy_question_label.x = SCREEN_WIDTH / 2 - easy_question_label.get_size()[0] / 2
        average_question_label.x = SCREEN_WIDTH / 2 - average_question_label.get_size()[0] / 2
        hard_question_label.x = SCREEN_WIDTH / 2 - hard_question_label.get_size()[0] / 2

        average_question_label.y = SCREEN_HEIGHT / 2 - average_question_label.get_size()[1] / 2
        easy_question_label.y = average_question_label.y + average_question_label.get_size()[1] + 10
        hard_question_label.y = average_question_label.y - hard_question_label.get_size()[1] - 10

        self._questions = [easy_question, average_question, hard_question]
        self._labels = [easy_question_label, average_question_label, hard_question_label]

        get_game().register('on_draw', self.on_draw)
        get_game().register('on_mouse_motion', self.on_mouse_motion)
        get_game().register('on_mouse_press', self.on_mouse_press)

    def show(self):
        super().show()
        self._selected_question = None

    def on_draw(self):
        if not self.is_visible:
            return

        if self._show_highlight:
            label = self._labels[self._highlighted_index]
            w, h = label.get_size()
            arcade.draw_rectangle_filled(label.x + w / 2, label.y + h / 2, w + 10, h + 10, arcade.color.ORANGE)

        for label in self._labels:
            label.on_draw()

    def on_mouse_motion(self, x, y, _dx, _dy):
        self._show_highlight = False
        for i, label in enumerate(self._labels):
            if is_point_in_rect(x, y, label.x, label.y, label.get_size()[0], label.get_size()[1]):
                self._show_highlight = True
                self._highlighted_index = i

    @property
    def selected_question(self):
        return self._selected_question

    @sleep_before(3)
    def _answer_question(self):
        get_game().current_contestant.answer()

    @sleep_before(1)
    def _show_selected_answer(self):
        self._selected_question = self._questions[self._highlighted_index]
        self.hide()
        get_game().unpause_gameplay()
        self._answer_question()

    def on_mouse_press(self,  _x, _y, button, _modifiers):
        if (button == arcade.MOUSE_BUTTON_LEFT) and self._show_highlight:
            get_game().pause_gameplay()
            self._show_selected_answer()
