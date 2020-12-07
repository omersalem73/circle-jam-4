import arcade

from globals import SCREEN_WIDTH, SCREEN_HEIGHT


class BackgroundController:

    def __init__(self):
        self._host_bg = arcade.load_texture("images/1_pixel.png")
        self._contestant_bg = arcade.load_texture("images/2_pixel.png")
        self._select_question_bg = arcade.load_texture("images/3_pixel.png")
        self._show_question_bg = arcade.load_texture("images/4_pixel.png")
        self._current_bg = self._select_question_bg

    def show_host(self):
        self._current_bg = self._host_bg

    def show_contestant(self):
        self._current_bg = self._contestant_bg

    def show_select_question(self):
        self._current_bg = self._select_question_bg

    def show_question(self):
        self._current_bg = self._show_question_bg

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self._current_bg)
