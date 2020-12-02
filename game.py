import arcade

from globals import timers, SCREEN_WIDTH, SCREEN_HEIGHT
from ui_base import CallbacksRegisterer
from question import Question, QuestionUI
from question_data import QuestionData, QuestionDifficulty
from question_pool import QuestionsPool
from contestant import Contestant
from questions_stages import QuestionsStages
from audience_share import AudienceShare
from budget import Budget
from background_controller import BackgroundController


class Game(arcade.Window, CallbacksRegisterer):

    def __init__(self):
        arcade.Window.__init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, fullscreen=False)
        CallbacksRegisterer.__init__(self)
        self._background_color = arcade.color.DARK_BLUE
        self._window_size = SCREEN_WIDTH, SCREEN_HEIGHT
        self._is_gameplay_paused = False
        self._on_screen_question = None
        self._on_screen_question_data = None
        self._questions_pool = None
        self._current_contestant = None
        self._questions_stages = None
        self._audience_share = None
        self._budget = None
        self._background_controller = None

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
        self._background_controller = BackgroundController()

        self._questions_pool.show()

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
    def on_screen_question_ui(self) -> QuestionUI:
        return self._on_screen_question.ui

    @property
    def questions_stages(self) -> QuestionsStages:
        return self._questions_stages

    @property
    def question_pool(self) -> QuestionsPool:
        return self._questions_pool

    @property
    def background_controller(self) -> BackgroundController:
        return self._background_controller

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
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self._background_controller.current_bg)
        CallbacksRegisterer.on_draw(self)

    def _calc_viewport_ratio(self):
        return SCREEN_WIDTH / self._window_size[0], SCREEN_HEIGHT / self._window_size[1]

    def on_mouse_press(self, x, y, button, modifiers):
        if self._is_gameplay_paused:
            return
        rx, ry = self._calc_viewport_ratio()
        CallbacksRegisterer.on_mouse_press(self, x * rx, y * ry, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self._is_gameplay_paused:
            return

        rx, ry = self._calc_viewport_ratio()
        CallbacksRegisterer.on_mouse_motion(self, x * rx, y * ry, dx, dy)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.set_fullscreen(False)
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
            self._window_size = self.get_size()
        elif symbol == arcade.key.F:
            self.set_fullscreen(True)
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
            self._window_size = self.get_size()
