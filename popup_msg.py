import arcade

from globals import SCREEN_WIDTH, SCREEN_HEIGHT, get_game
from question_data import QuestionDifficulty
from ui_base import VisibilityToggle
from text_box import TextBox
from button import Button

BORDER = 3


class PopupMessage(VisibilityToggle):

    def __init__(self):
        super().__init__(is_visible=True)
        self._text_box = TextBox(self.format_msg(), SCREEN_WIDTH / 2 - 20, SCREEN_WIDTH / 4 + 10, SCREEN_HEIGHT * 0.75 - 10)
        self._continue_btn = Button('Continue', 0, SCREEN_HEIGHT / 4 + 10, lambda: self._on_click_continue())
        self._continue_btn.x = SCREEN_WIDTH * 0.75 - self._continue_btn.get_size()[0] - 20
        get_game().register('on_draw', self.on_draw)
        get_game().register_button_mouse_events(self._continue_btn)

    @staticmethod
    def format_msg():
        contestant = get_game().current_contestant
        return (
            '-- New Contestant --\n'
            f'Name: {contestant.name}\n'
            f'Chance of answering easy questions: {contestant.answer_prob[QuestionDifficulty.EASY]}\n'
            f'Chance of answering average questions: {contestant.answer_prob[QuestionDifficulty.AVERAGE]}\n'
            f'Chance of answering hard questions: {contestant.answer_prob[QuestionDifficulty.HARD]}\n'
            f'Chance of contestant withdrawal: #TODO\n'
            '\nTotal profit +/- this round: +30000\n'
            'Total rating +/- this round: +2.75'
        )

    def _on_click_continue(self):
        self.hide()
        get_game().question_pool.show()

    def show(self):
        super().show()
        get_game().disable_all_buttons()
        self._continue_btn.enable()

    def draw_if_visible(self):
        self._text_box.text = self.format_msg()
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH / 4 - BORDER, SCREEN_HEIGHT / 4 - BORDER, BORDER,
                                          SCREEN_HEIGHT / 2 + BORDER, arcade.color.LIGHT_SKY_BLUE)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH / 4 - BORDER, SCREEN_HEIGHT / 4 - BORDER,
                                          SCREEN_WIDTH / 2 + BORDER, BORDER, arcade.color.LIGHT_SKY_BLUE)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH / 4 - BORDER, SCREEN_HEIGHT * 0.75,
                                          SCREEN_WIDTH / 2 + BORDER, BORDER, arcade.color.LIGHT_SKY_BLUE)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT / 4 - BORDER,
                                          BORDER, SCREEN_HEIGHT / 2 + BORDER * 2, arcade.color.LIGHT_SKY_BLUE)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                          (0, 0, 0, 230))
        self._text_box.on_draw()
        self._continue_btn.on_draw()
