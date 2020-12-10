import arcade

from globals import SCREEN_WIDTH, SCREEN_HEIGHT, get_game
from question_data import QuestionDifficulty
from ui_base import VisibilityToggle
from text_box import TextBox
from button import Button

BORDER = 3
PADDING = 10
HEIGHT = SCREEN_HEIGHT * 0.4


class PopupMessage(VisibilityToggle):

    def __init__(self):
        super().__init__(is_visible=True)
        self._text_box = TextBox('', SCREEN_WIDTH / 4 + 10, 0, bounds_w=SCREEN_WIDTH / 2 - 20,
                                 font_size=18)
        self._on_continue_callback = None
        self._continue_btn = Button('Continue', 0, 0, lambda: self._on_click_continue())
        self._continue_btn.x = SCREEN_WIDTH * 0.75 - self._continue_btn.get_size()[0] - 20
        get_game().register('on_draw', self.on_draw)
        get_game().register_button_mouse_events(self._continue_btn)

        self._rect_y = 0
        self._rect_h = 0
        self.set_text(self.new_contestant_message())

    @staticmethod
    def new_contestant_message():
        contestant = get_game().current_contestant
        easy_answer_percent = '{}%'.format(int(contestant.answer_prob[QuestionDifficulty.EASY] * 100))
        average_answer_percent = '{}%'.format(int(contestant.answer_prob[QuestionDifficulty.AVERAGE] * 100))
        hard_answer_percent = '{}%'.format(int(contestant.answer_prob[QuestionDifficulty.HARD] * 100))
        prize_to_quit_percent = {
            16000: '{}%'.format(int(contestant.prize_to_quit_prob[16000] * 100)),
            125000: '{}%'.format(int(contestant.prize_to_quit_prob[125000] * 100))
        }
        return (
            f'Name: {contestant.name}\n'
            f'Chance of answering easy questions: {easy_answer_percent}\n'
            f'Chance of answering average questions: {average_answer_percent}\n'
            f'Chance of answering hard questions: {hard_answer_percent}\n'
            f'Chances of withdrawal: {prize_to_quit_percent[16000]} on $16000, {prize_to_quit_percent[125000]} on $125000'
        )

    @staticmethod
    def contestant_lost_message():
        contestant = get_game().current_contestant
        prize_money = get_game().questions_stages.get_current_prize_money()
        return (
            f'{contestant.name} lost the ${prize_money} question!\n'
            f'Total profit this round: {get_game().budget.get_diff_sum()}\n'
            f'Total rating this round: {get_game().audience_share.get_diff_sum()}'
        )

    @staticmethod
    def contestant_withdrawn_message():
        contestant = get_game().current_contestant
        prize_money = get_game().questions_stages.get_current_prize_money()
        return (
            f'{contestant.name} withdrawn with ${prize_money}!\n'
            f'Total profit this round: {get_game().budget.get_diff_sum()}\n'
            f'Total rating this round: {get_game().audience_share.get_diff_sum()}'
        )

    @staticmethod
    def contestant_won_message():
        contestant = get_game().current_contestant
        return (
            f'{contestant.name} won the MILLION DOLLARS PRIZE!!!\n'
            'Sadly for you...\n'
            f'Total profit this round: {get_game().budget.get_diff_sum()}\n'
            f'Total rating this round: {get_game().audience_share.get_diff_sum()}'
        )

    @staticmethod
    def player_won_message():
        return (
            f'You WON!!!\n'
            f'You are a successful game show runner!\n'
        )

    @staticmethod
    def player_lost_message():
        return (
            f'You lost...\n'
            f'Better luck next time...\n'
        )

    def _on_click_continue(self):
        self.hide()
        if self._on_continue_callback:
            self._on_continue_callback()

    def set_text(self, text):
        self._text_box.text = text
        text_h = self._text_box.get_size()[1]
        self._text_box.y = SCREEN_HEIGHT * 0.75 + text_h / 2
        self._rect_h = PADDING + text_h + PADDING + self._continue_btn.get_size()[1] + PADDING
        self._rect_y = self._text_box.y - self._rect_h + PADDING
        self._continue_btn.y = self._rect_y + PADDING

    def show(self, on_continue_callback=None):
        super().show()
        self._on_continue_callback = on_continue_callback
        get_game().disable_all_buttons()
        self._continue_btn.enable()

    def draw_if_visible(self):
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH / 4 - BORDER, self._rect_y - BORDER, BORDER,
                                          self._rect_h + BORDER, arcade.color.LIGHT_SKY_BLUE)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH / 4 - BORDER, self._rect_y - BORDER,
                                          SCREEN_WIDTH / 2 + BORDER, BORDER, arcade.color.LIGHT_SKY_BLUE)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH / 4 - BORDER, self._rect_y + self._rect_h,
                                          SCREEN_WIDTH / 2 + BORDER, BORDER, arcade.color.LIGHT_SKY_BLUE)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH * 0.75, self._rect_y - BORDER,
                                          BORDER, self._rect_h + BORDER * 2, arcade.color.LIGHT_SKY_BLUE)
        arcade.draw_xywh_rectangle_filled(SCREEN_WIDTH / 4, self._rect_y, SCREEN_WIDTH / 2, self._rect_h,
                                          (0, 0, 0, 230))
        self._text_box.on_draw()
        self._continue_btn.on_draw()
