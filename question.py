import arcade

from globals import get_game, sleep_before, SCREEN_WIDTH
from question_data import QuestionData
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
        letters = ['A', 'B', 'C', 'D']
        for i, answer in enumerate(answers):
            lbl = self._answer_labels[i]
            lbl.text = '{}: {}'.format(letters[i], answer)
            if (i == 0) or (i == 2):
                lbl.x = 210 * SCREEN_WIDTH / 2 / self._left_answer_bg.width
            else:
                lbl.x = SCREEN_WIDTH / 2 + 120 * SCREEN_WIDTH / 2 / self._right_answer_bg.width
            if (i == 0) or (i == 1):
                lbl.y = self._upper_answer_y - lbl.get_size()[1] / 2
            else:
                lbl.y = self._lower_answer_y - lbl.get_size()[1] / 2

    def mark_as_correct(self, i):
        if (i == 0) or (i == 2):
            self._answers_bgs[i] = self._left_answer_correct_bg
        else:
            self._answers_bgs[i] = self._right_answer_correct_bg
        self._answer_labels[i].color = arcade.color.BLACK

    def select(self, i):
        if (i == 0) or (i == 2):
            self._answers_bgs[i] = self._left_answer_selected_bg
        else:
            self._answers_bgs[i] = self._right_answer_selected_bg
        self._answer_labels[i].color = arcade.color.BLACK

    def unselect(self, i):
        if (i == 0) or (i == 2):
            self._answers_bgs[i] = self._left_answer_bg
        else:
            self._answers_bgs[i] = self._right_answer_bg
        self._answer_labels[i].color = arcade.color.WHITE

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

    def __init__(self, index, ui: QuestionUI):
        self._index = index
        self._ui = ui
        self._is_selected = False

    def select(self):
        self._ui.select(self._index)
        self._is_selected = True

    def mark_as_correct(self):
        self._ui.mark_as_correct(self._index)

    def unselect(self):
        self._ui.unselect(self._index)
        self._is_selected = False

    @property
    def is_selected(self):
        return self._is_selected


class Question:

    def __init__(self):
        self._question_data = None
        self._ui = QuestionUI()
        self._answers = [PossibleAnswer(i, self._ui) for i in range(4)]
        self._correct_answer_index = -1
        get_game().register('on_draw', self.on_draw)

    def update_data(self, question_data: QuestionData):
        self._question_data = question_data
        self._correct_answer_index = randint(0, 3)
        answers = [question_data.correct_answer] + question_data.three_wrong_answers
        answers[0], answers[self._correct_answer_index] = answers[self._correct_answer_index], answers[0]
        self._ui.set_texts(question_data.text, answers)

    def reset_data(self):
        if self._correct_answer_index != -1:
            self._get_selected_answer().unselect()
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
        return [ans for ans in self._answers if ans.is_selected][0]

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
