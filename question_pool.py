import random
from globals import SCREEN_WIDTH, get_game, sleep_before, add_timer
from ui_base import VisibilityToggle
from label import Label
from button import Button


class QuestionsPool(VisibilityToggle):

    def __init__(self, easy_questions, average_questions, hard_questions):
        super().__init__(is_visible=False)
        self._show_highlight = False
        self._highlighted_index = 0
        self._selected_question = None

        self._choose_question_label = Label("Choose a question difficulty:", 0, 0)
        easy_question_label = Button('Easy', 0, 0, lambda: self._on_difficulty_clicked(0))
        average_question_label = Button('Average', 0, 0, lambda: self._on_difficulty_clicked(1))
        hard_question_label = Button('Hard', 0, 0, lambda: self._on_difficulty_clicked(2))

        total_w = self._choose_question_label.get_size()[0] + 25 + easy_question_label.get_size()[0] + 25 + \
            average_question_label.get_size()[0] + 25 + hard_question_label.get_size()[0]

        self._choose_question_label.x = SCREEN_WIDTH / 2 - total_w / 2
        easy_question_label.x = self._choose_question_label.x + self._choose_question_label.get_size()[0] + 25
        average_question_label.x = easy_question_label.x + easy_question_label.get_size()[0] + 25
        hard_question_label.x = average_question_label.x + average_question_label.get_size()[0] + 25

        self._questions = [easy_questions, average_questions, hard_questions]
        self._buttons = [easy_question_label, average_question_label, hard_question_label]

        get_game().register('on_draw', self.on_draw)

        for btn in self._buttons:
            get_game().register_button_mouse_events(btn)

    def _on_difficulty_clicked(self, index):
        get_game().pause_gameplay()
        [
            get_game().sound_controller.play_select_easy,
            get_game().sound_controller.play_select_average,
            get_game().sound_controller.play_select_hard
        ][index]()
        self._show_selected_answer(index)

    def show(self):
        super().show()
        get_game().disable_all_buttons()
        self._selected_question = None
        self._choose_question_label.y = get_game().on_screen_question_ui.get_question_box_y() - \
            self._choose_question_label.get_size()[1] / 2
        for btn in self._buttons:
            btn.y = self._choose_question_label.y
            btn.enable()

    def draw_if_visible(self):
        self._choose_question_label.on_draw()
        for btn in self._buttons:
            btn.on_draw()

    @property
    def selected_question(self):
        return self._selected_question

    @sleep_before(3)
    def _answer_question(self):
        question = get_game().on_screen_question
        get_game().current_contestant.answer(question)
        question.verify_answered_question()

    @sleep_before(0.1)
    def _show_selected_answer(self, index):
        self._selected_question = random.choice(self._questions[index])
        self.hide()
        get_game().background_controller.show_host()
        get_game().questions_stages.hide()
        get_game().unpause_gameplay()
        add_timer(1, lambda: get_game().background_controller.show_question())
        add_timer(2, lambda: get_game().background_controller.show_contestant())
        self._answer_question()
