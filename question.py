import arcade

from globals import get_game, sleep_before
from ui_base import is_point_in_rect
from random import randint


class PossibleAnswer:

    def __init__(self, tile_x, tile_y):
        self._tile_x = tile_x
        self._tile_y = tile_y
        self._text = ''
        self._color = arcade.color.RED

    def set_text(self, text):
        self._text = text

    def select(self):
        self._color = arcade.color.YELLOW

    def mark_as_correct(self):
        self._color = arcade.color.GREEN

    def unselect(self):
        self._color = arcade.color.RED

    def is_selected(self):
        return self._color == arcade.color.YELLOW

    def on_draw(self):
        arcade.draw_rectangle_filled(300 + 600 * self._tile_x, 40 + 80 * self._tile_y, 600, 80, self._color)
        arcade.draw_text(self._text, 300 + 600 * self._tile_x, 40 + 80 * self._tile_y, arcade.color.WHITE, 26,
                         anchor_x='center')

    def on_mouse_press(self, x, y, button, _modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if is_point_in_rect(x, y, 600 * self._tile_x, 80 * self._tile_y, 600, 80):
                self.select()


class Question:

    def __init__(self):
        self._text = ''
        self._answers = [
            PossibleAnswer(0, 0),
            PossibleAnswer(1, 0),
            PossibleAnswer(0, 1),
            PossibleAnswer(1, 1)
        ]
        self._correct_answer_index = -1
        get_game().register('on_draw', self.on_draw)

    def update_data(self, question_data):
        self._text = question_data.text
        self._correct_answer_index = randint(0, 3)
        self.get_correct_answer().set_text(question_data.correct_answer)
        for wrong_answer, wrong_answer_text in zip(self.get_wrong_answers(), question_data.three_wrong_answers):
            wrong_answer.set_text(wrong_answer_text)

    def reset_data(self):
        self._text = ''
        for answer in self._answers:
            answer.set_text('')
            answer.unselect()
        self._correct_answer_index = -1

    def on_draw(self):
        if self._correct_answer_index == -1:
            return

        arcade.draw_rectangle_filled(600, 40 + 80 * 2, 600, 80, arcade.color.BLUE)
        arcade.draw_text(self._text, 600, 40 + 80 * 2, arcade.color.WHITE, 26,
                         anchor_x='center')
        for answer in self._answers:
            answer.on_draw()

    def get_correct_answer(self):
        return self._answers[self._correct_answer_index]

    def get_wrong_answers(self):
        return [ans for i, ans in enumerate(self._answers) if i != self._correct_answer_index]

    def _get_selected_answer(self):
        return [ans for ans in self._answers if ans.is_selected()][0]

    @sleep_before(2)
    def verify_answered_question(self):
        selected = self._get_selected_answer()
        correct = self.get_correct_answer()
        correct.mark_as_correct()

        if selected == correct:
            get_game().questions_stages.next_stage()
        else:
            get_game()
