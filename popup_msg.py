import arcade

from globals import SCREEN_WIDTH, SCREEN_HEIGHT, get_game
from ui_base import VisibilityToggle
from text_box import TextBox
from button import Button

BORDER = 3
NEW_CONTESTANT_TEXT = '-- New Contestant --\nName: Omer Salem\nChance of answering easy questions: 0.5\nChance of ' \
                      'answering average questions: 0.5\nChance of answering hard questions: 0.5\nChance of ' \
                      'contestant withdrawal: 0.5\n\nTotal profit +/- this round: +30000\nTotal rating +/- this ' \
                      'round: +2.75 '


class PopupMessage(VisibilityToggle):

    def __init__(self):
        super().__init__(is_visible=True)
        self._text_box = TextBox(NEW_CONTESTANT_TEXT, SCREEN_WIDTH / 2 - 20,
                                 SCREEN_WIDTH / 4 + 10, SCREEN_HEIGHT * 0.75 - 10)
        self._on_continue_callback = None
        self._continue_btn = Button('Continue', 0, SCREEN_HEIGHT / 4 + 10, lambda: self._on_click_continue())
        self._continue_btn.x = SCREEN_WIDTH * 0.75 - self._continue_btn.get_size()[0] - 20
        get_game().register('on_draw', self.on_draw)
        get_game().register_button_mouse_events(self._continue_btn)

    def _on_click_continue(self):
        self.hide()
        if self._on_continue_callback:
            self._on_continue_callback()

    def set_text(self, text):
        self._text_box.text = text

    def show(self, on_continue_callback=None):
        super().show()
        self._on_continue_callback = on_continue_callback
        get_game().disable_all_buttons()
        self._continue_btn.enable()

    def draw_if_visible(self):
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
