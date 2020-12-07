import random

import arcade

from contestant_finish_message import ContestantFinishMessage
from globals import timers, SCREEN_WIDTH, SCREEN_HEIGHT, add_timer
from questions_data import questions_data
from ui_base import CallbacksRegisterer
from question import Question, QuestionUI
from question_data import QuestionData, QuestionDifficulty
from question_pool import QuestionsPool
from contestant import Contestant
from questions_stages import QuestionsStages
from audience_share import AudienceShare
from budget import Budget
from background_controller import BackgroundController
from popup_msg import PopupMessage


class Game(arcade.Window, CallbacksRegisterer):

    POSSIBLE_CONTESTANTS = [
        Contestant(
            'Daniyal Mcgregor',
            answer_prob={
                QuestionDifficulty.HARD: 0.3,
                QuestionDifficulty.AVERAGE: 0.7,
                QuestionDifficulty.EASY: 0.86
            },
            prize_to_quit_prob={
                1000: 0.3,
                32000: 0.7
            }
        ),
        Contestant(
            'Susan Cardenas',
            answer_prob={
                QuestionDifficulty.HARD: 0.5,
                QuestionDifficulty.AVERAGE: 0.8,
                QuestionDifficulty.EASY: 0.9
            },
            prize_to_quit_prob={
                1000: 0.1,
                32000: 0.6
            }
        ),
        Contestant(
            'Theo Paul',
            answer_prob={
                QuestionDifficulty.HARD: 0.1,
                QuestionDifficulty.AVERAGE: 0.8,
                QuestionDifficulty.EASY: 0.6
            },
            prize_to_quit_prob={
                1000: 0.6,
                32000: 0.8
            }
        ),
        Contestant(
            'Lynda Fowler',
            answer_prob={
                QuestionDifficulty.HARD: 0.35,
                QuestionDifficulty.AVERAGE: 0.7,
                QuestionDifficulty.EASY: 0.9
            },
            prize_to_quit_prob={
                1000: 0.7,
                32000: 0.9
            }
        ),
        Contestant(
            'Antonio Kenny',
            answer_prob={
                QuestionDifficulty.HARD: 0.65,
                QuestionDifficulty.AVERAGE: 0.8,
                QuestionDifficulty.EASY: 0.9
            },
            prize_to_quit_prob={
                1000: 0.3,
                32000: 0.4
            }
        )
    ]

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
        self._contestant_finish_message = None
        self._background_controller = None
        self._popup_message = None

    def init(self):
        self._budget = Budget()
        self._audience_share = AudienceShare()
        self._contestant_finish_message = ContestantFinishMessage()
        self._on_screen_question = Question()
        self._questions_pool = QuestionsPool(*questions_data)
        self._questions_stages = QuestionsStages()
        self._background_controller = BackgroundController()
        self._current_contestant = random.choice(type(self).POSSIBLE_CONTESTANTS)
        self._popup_message = PopupMessage()
        self._popup_message.show()

    def next_contestant(self):
        self._current_contestant = random.choice(type(self).POSSIBLE_CONTESTANTS)
        self._questions_stages.reset()
        add_timer(3, self._popup_message.show)

    @property
    def audience_share(self) -> AudienceShare:
        return self._audience_share

    @property
    def budget(self) -> Budget:
        return self._budget

    @property
    def contestant_finish_message(self) -> ContestantFinishMessage:
        return self._contestant_finish_message

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

    def player_won(self):
        self.pause_gameplay()

    def player_lost(self):
        self.pause_gameplay()

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

        if self._is_gameplay_paused:
            return
        CallbacksRegisterer.on_update(self, delta_time)

    def on_draw(self):
        arcade.start_render()
        self._background_controller.on_draw()
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
