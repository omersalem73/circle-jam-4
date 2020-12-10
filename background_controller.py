import arcade

from globals import SCREEN_WIDTH, SCREEN_HEIGHT


class BackgroundController:

    def __init__(self):
        self._contestant_bgs = [arcade.load_texture("images/contestant_{}.png".format(i + 1)) for i in range(3)]
        self._select_question_bgs = [arcade.load_texture("images/select_question_{}.png".format(i + 1)) for i in range(3)]
        self._show_question_bgs = [arcade.load_texture("images/show_question_{}.png".format(i + 1)) for i in range(3)]

        self._host_bg = arcade.load_texture("images/host.png")
        self._contestant_bg = None
        self._select_question_bg = None
        self._show_question_bg = None
        self._current_bg = None

    def set_index(self, index):
        self._contestant_bg = self._contestant_bgs[index]
        self._select_question_bg = self._select_question_bgs[index]
        self._show_question_bg = self._show_question_bgs[index]
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
