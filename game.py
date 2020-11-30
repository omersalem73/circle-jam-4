import arcade

from globals import timers, SCREEN_WIDTH, SCREEN_HEIGHT, get_game
from ui_base import CallbacksRegisterer
from question import Question
from question_data import QuestionData, QuestionDifficulty
from question_pool import QuestionsPool
from contestant import Contestant
from questions_stages import QuestionsStages
from audience_share import AudienceShare
from budget import Budget


class Game(arcade.Window, CallbacksRegisterer):

    def __init__(self):
        arcade.Window.__init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, fullscreen=True)
        CallbacksRegisterer.__init__(self)
        self._is_gameplay_paused = False
        self._on_screen_question = None
        self._on_screen_question_data = None
        self._questions_pool = None
        self._current_contestant = None
        self._questions_stages = None
        self._audience_share = None
        self._budget = None

    def init(self):
        self._budget = Budget()
        self._audience_share = AudienceShare()
        self._on_screen_question = Question()
        self._questions_pool = QuestionsPool(*[
            QuestionData(
                'Who has the biggest?',
                'Omer',
                ['Shoded', 'Omri', 'Gonen'],
                QuestionDifficulty.EASY
            ),
            QuestionData(
                'Who has the longest?',
                'Omer',
                ['Shoded', 'Omri', 'Gonen'],
                QuestionDifficulty.AVERAGE
            ),
            QuestionData(
                'Who has the hardest?',
                'Omer',
                ['Shoded', 'Omri', 'Gonen'],
                QuestionDifficulty.HARD
            )
        ])
        self._questions_stages = QuestionsStages()
        self._current_contestant = Contestant()

    @property
    def audience_share(self) -> AudienceShare:
        return self._audience_share

    @property
    def budget(self) -> Budget:
        return self._budget

    @property
    def current_contestant(self) -> Contestant:
        return self._current_contestant

    @property
    def on_screen_question(self) -> Question:
        return self._on_screen_question

    @property
    def questions_stages(self) -> QuestionsStages:
        return self._questions_stages

    @property
    def question_pool(self) -> QuestionsPool:
        return self._questions_pool

    def pause_gameplay(self):
        self._is_gameplay_paused = True

    def unpause_gameplay(self):
        self._is_gameplay_paused = False

    def on_update(self, delta_time: float):
        for timer in timers[:]:
            timer.tick(delta_time)
            if timer.was_called:
                timers.remove(timer)

        new_selected_question = self._questions_pool.selected_question
        if new_selected_question != self._on_screen_question_data:
            self._on_screen_question_data = new_selected_question
            if new_selected_question:
                self._on_screen_question.update_data(new_selected_question)

    def on_draw(self):
        arcade.start_render()
        CallbacksRegisterer.on_draw(self)

    def on_mouse_press(self, x, y, button, modifiers):
        if self._is_gameplay_paused:
            return
        CallbacksRegisterer.on_mouse_press(self, x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self._is_gameplay_paused:
            return
        CallbacksRegisterer.on_mouse_motion(self, x, y, dx, dy)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.set_fullscreen(False)
        elif symbol == arcade.key.F:
            self.set_fullscreen(True)
