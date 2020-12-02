import arcade


class BackgroundController:

    def __init__(self):
        self._host_bg = arcade.load_texture("images/1_pixel.png")
        self._contestant_bg = arcade.load_texture("images/2_pixel.png")
        self._select_question_bg = arcade.load_texture("images/3_pixel.png")
        self._show_question_bg = arcade.load_texture("images/4_pixel.png")
        self._current_bg = self._select_question_bg

    @property
    def current_bg(self):
        return self._current_bg

    def show_host(self):
        self._current_bg = self._host_bg

    def show_contestant(self):
        self._current_bg = self._contestant_bg

    def show_select_question(self):
        self._current_bg = self._select_question_bg

    def show_question(self):
        self._current_bg = self._show_question_bg
