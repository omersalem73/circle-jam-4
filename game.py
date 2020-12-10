import random

import arcade

from globals import timers, SCREEN_WIDTH, SCREEN_HEIGHT, sleep_before, add_timer
from questions_data import questions_data
from sound_controller import SoundController
from ui_base import CallbacksRegisterer
from question import Question, QuestionUI
from question_data import QuestionDifficulty
from question_pool import QuestionsPool
from contestant import Contestant
from questions_stages import QuestionsStages
from audience_share import AudienceShare
from budget import Budget, WIN_BUDGET, LOSE_BUDGET
from background_controller import BackgroundController
from popup_msg import PopupMessage


class Game(arcade.Window, CallbacksRegisterer):

    BASE_SHOW_COST = 50000

    POSSIBLE_CONTESTANTS = [
        Contestant(
            'Daniela Mcgregor',
            answer_prob={
                QuestionDifficulty.HARD: 0.3,
                QuestionDifficulty.AVERAGE: 0.7,
                QuestionDifficulty.EASY: 0.86
            },
            prize_to_quit_prob={
                16000: 0.3,
                125000: 0.7
            },
            bg_images_index=0
        ),
        Contestant(
            'Susan Cardenas',
            answer_prob={
                QuestionDifficulty.HARD: 0.5,
                QuestionDifficulty.AVERAGE: 0.8,
                QuestionDifficulty.EASY: 0.9
            },
            prize_to_quit_prob={
                16000: 0.1,
                125000: 0.6
            },
            bg_images_index=2
        ),
        Contestant(
            'Theo Paul',
            answer_prob={
                QuestionDifficulty.HARD: 0.1,
                QuestionDifficulty.AVERAGE: 0.6,
                QuestionDifficulty.EASY: 0.8
            },
            prize_to_quit_prob={
                16000: 0.0,
                125000: 0.1
            },
            bg_images_index=1
        ),
        Contestant(
            'Lynda Fowler',
            answer_prob={
                QuestionDifficulty.HARD: 0.35,
                QuestionDifficulty.AVERAGE: 0.7,
                QuestionDifficulty.EASY: 0.9
            },
            prize_to_quit_prob={
                16000: 0.7,
                125000: 0.9
            },
            bg_images_index=0
        ),
        Contestant(
            'Antonio Kenny',
            answer_prob={
                QuestionDifficulty.HARD: 0.65,
                QuestionDifficulty.AVERAGE: 0.8,
                QuestionDifficulty.EASY: 0.9
            },
            prize_to_quit_prob={
                16000: 0.3,
                125000: 0.4
            },
            bg_images_index=1
        )
    ]

    def __init__(self):
        arcade.Window.__init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, fullscreen=False)
        CallbacksRegisterer.__init__(self)
        self._splash_screen = arcade.load_texture("images/logo.png")
        self._is_splash_screen_visible = True
        self._window_size = SCREEN_WIDTH, SCREEN_HEIGHT
        self._is_gameplay_paused = True
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
        self._game_ended = False
        self._sound_controller = None

    def init(self):
        self._splash_screen = arcade.load_texture("images/logo.png")
        self._budget = Budget()
        self._audience_share = AudienceShare()
        self._on_screen_question = Question()
        self._questions_pool = QuestionsPool(*questions_data)
        self._questions_stages = QuestionsStages()
        self._background_controller = BackgroundController()
        self._current_contestant = random.choice(type(self).POSSIBLE_CONTESTANTS)
        self._popup_message = PopupMessage()
        self._sound_controller = SoundController()

        self._sound_controller.play_theme_in_loop()
        self._background_controller.set_index(self.current_contestant.bg_images_index)
        self.question_pool.show()
        self._popup_message.show(on_continue_callback=self._popup_next_contestant_callback)

        add_timer(3, self._after_splash_screen)

    def _after_splash_screen(self):
        self._is_splash_screen_visible = False
        self._is_gameplay_paused = False

    def _popup_next_contestant_callback(self):
        self.question_pool.show()

    @sleep_before(1)
    def next_contestant(self):
        self.budget.lose_amount(type(self).BASE_SHOW_COST)
        self.audience_share.reset(diff_only=True)
        self.background_controller.show_select_question()
        self._current_contestant = random.choice(type(self).POSSIBLE_CONTESTANTS)
        self.questions_stages.reset()
        self.on_screen_question.reset_data()

        self._background_controller.set_index(self.current_contestant.bg_images_index)
        self.questions_stages.show()
        self.question_pool.show()

        self._popup_message.set_text(PopupMessage.new_contestant_message())
        self._popup_message.show(on_continue_callback=self._popup_next_contestant_callback)

    @sleep_before(1)
    def new_game(self):
        self.budget.reset()
        self.audience_share.reset()
        self.next_contestant()
        self._game_ended = False

    @property
    def sound_controller(self) -> SoundController:
        return self._sound_controller

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

    def _check_if_player_lost_or_won(self):
        if self.budget.get() == WIN_BUDGET:
            self.player_won()
            return True
        elif self.budget.get() == LOSE_BUDGET:
            self.player_lost()
            return True
        return False

    def next_stage_or_new_contestant(self):
        self.audience_share.update(self.on_screen_question.question_data)
        if self.on_screen_question.is_selected_answer_correct():
            if self.questions_stages.is_current_question_last():
                self._popup_message.set_text(PopupMessage.contestant_won_message())
                self.budget.lose_amount(self.questions_stages.get_current_prize_money())
            elif self.current_contestant.should_withdraw():
                self.budget.lose_amount(self.questions_stages.get_current_prize_money())
                self._popup_message.set_text(PopupMessage.contestant_withdrawn_message())
            else:
                if self._check_if_player_lost_or_won():
                    return
                self.questions_stages.next_stage()
                return
        else:
            self._popup_message.set_text(PopupMessage.contestant_lost_message())

        if self._check_if_player_lost_or_won():
            return
        self._popup_message.show(on_continue_callback=lambda: self.next_contestant())

    def pause_gameplay(self):
        self._is_gameplay_paused = True

    def unpause_gameplay(self):
        self._is_gameplay_paused = False

    def player_won(self):
        self._game_ended = True
        self._popup_message.set_text(PopupMessage.player_won_message())
        self._popup_message.show(on_continue_callback=lambda: self.new_game())

    def player_lost(self):
        self._game_ended = True
        self._popup_message.set_text(PopupMessage.player_lost_message())
        self._popup_message.show(on_continue_callback=lambda: self.new_game())

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

        if self._is_splash_screen_visible:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self._splash_screen)

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
