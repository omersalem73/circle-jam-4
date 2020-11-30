import arcade

from globals import get_game, sleep_before, SCREEN_WIDTH
from question_data import QuestionData
from ui_base import is_point_in_rect
from label import Label
from random import randint


class QuestionUI:

    BOTTOM_MARGIN = 30

    def __init__(self):
        self._question_bg = arcade.load_texture("images/question.png")
        self._left_answer_bg = arcade.load_texture("images/answer_left.png")
        self._left_answer_selected_bg = arcade.load_texture("images/answer_left_selected.png")
        self._left_answer_correct_bg = arcade.load_texture("images/answer_left_correct.png")
        self._right_answer_bg = arcade.load_texture("images/answer_right.png")
        self._right_answer_selected_bg = arcade.load_texture("images/answer_right_selected.png")
        self._right_answer_correct_bg = arcade.load_texture("images/answer_right_correct.png")
        self._question_label = Label('', 0, 0)
        self._answer_labels = [Label('', 0, 0) for _ in range(4)]

        self._question_ratio = self._question_bg.width / self._question_bg.height
        self._question_height = SCREEN_WIDTH / self._question_ratio
        self._answer_ratio = self._left_answer_bg.width / self._left_answer_bg.height
        self._answer_height = SCREEN_WIDTH / 2 / self._answer_ratio

        self._lower_answer_y = self._answer_height / 2 + QuestionUI.BOTTOM_MARGIN
        self._upper_answer_y = self._lower_answer_y + self._answer_height + 5
        self._question_y = QuestionUI.BOTTOM_MARGIN + self._answer_height * 2 + 5 + self._question_height / 2 + 5

        self._answers_bgs = [self._left_answer_bg, self._right_answer_bg, self._left_answer_bg, self._right_answer_bg]

    def set_texts(self, question, answers):
        self._question_label.text = question
        self._question_label.x = SCREEN_WIDTH / 2 - self._question_label.get_size()[0] / 2
        self._question_label.y = self._question_y - self._question_label.get_size()[1] / 2
        for i, answer in enumerate(answers):
            lbl = self._answer_labels[i]
            lbl.text = answer
            if (i == 0) or (i == 2):
                lbl.x = SCREEN_WIDTH / 4 - lbl.get_size()[0] / 2
            else:
                lbl.x = SCREEN_WIDTH / 4 * 3 - lbl.get_size()[0] / 2
            if (i == 0) or (i == 1):
                lbl.y = self._upper_answer_y - lbl.get_size()[1] / 2
            else:
                lbl.y = self._lower_answer_y - lbl.get_size()[1] / 2

    def mark_as_correct(self, i):
        if (i == 0) or (i == 2):
            self._answers_bgs[i] = self._left_answer_correct_bg
        else:
            self._answers_bgs[i] = self._right_answer_correct_bg

    def select(self, i):
        if (i == 0) or (i == 2):
            self._answers_bgs[i] = self._left_answer_selected_bg
        else:
            self._answers_bgs[i] = self._right_answer_selected_bg

    def unselect(self, i):
        if (i == 0) or (i == 2):
            self._answers_bgs[i] = self._left_answer_bg
        else:
            self._answers_bgs[i] = self._right_answer_bg

    def on_draw(self):
        h = self._answer_height
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 4, self._upper_answer_y, SCREEN_WIDTH / 2, h,
                                      self._answers_bgs[0])
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 4 * 3, self._upper_answer_y, SCREEN_WIDTH / 2,  h,
                                      self._answers_bgs[1])
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 4, self._lower_answer_y, SCREEN_WIDTH / 2, h,
                                      self._answers_bgs[2])
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 4 * 3, self._lower_answer_y, SCREEN_WIDTH / 2, h,
                                      self._answers_bgs[3])
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, self._question_y, SCREEN_WIDTH, self._question_height,
                                      self._question_bg)
        self._question_label.on_draw()
        for lbl in self._answer_labels:
            lbl.on_draw()


class PossibleAnswer:

    def __init__(self, tile_x, tile_y):
        self._tile_x = tile_x
        self._tile_y = tile_y
        self._text = ''
        self._label = Label('', 0, 0)
        self._color = arcade.color.RED

    def set_text(self, text):
        self._text = text
        self._label.text = text

    def select(self):
        self._color = arcade.color.YELLOW

    def mark_as_correct(self):
        self._color = arcade.color.GREEN

    def unselect(self):
        self._color = arcade.color.RED

    def is_selected(self):
        return self._color == arcade.color.YELLOW

    def on_draw(self):
        self._label.on_draw()
        arcade.draw_text(self._text, 300 + 600 * self._tile_x, 40 + 80 * self._tile_y, arcade.color.WHITE, 26,
                         anchor_x='center')

    def on_mouse_press(self, x, y, button, _modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if is_point_in_rect(x, y, 600 * self._tile_x, 80 * self._tile_y, 600, 80):
                self.select()


class Question:

    def __init__(self):
        self._text = ''
        self._question_data = None
        self._answers = [
            PossibleAnswer(0, 0),
            PossibleAnswer(1, 0),
            PossibleAnswer(0, 1),
            PossibleAnswer(1, 1)
        ]
        self._correct_answer_index = -1
        self._ui = QuestionUI()
        get_game().register('on_draw', self.on_draw)

    def update_data(self, question_data: QuestionData):
        self._question_data = question_data
        self._text = question_data.text
        self._ui.set_texts(question_data.text, [question_data.correct_answer] + question_data.three_wrong_answers)
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

        self._ui.on_draw()

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
            get_game().questions_stages.reset()

    @property
    def question_data(self) -> QuestionData:
        return self._question_data
