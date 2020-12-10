import arcade


class SoundController:

    def __init__(self):
        self._theme = arcade.sound.Sound('sound/theme.wav')
        self._select_easy = arcade.sound.Sound('sound/select_easy.wav')
        self._select_average = arcade.sound.Sound('sound/select_average.wav')
        self._select_hard = arcade.sound.Sound('sound/select_hard.wav')

    def play_theme_in_loop(self):
        self._theme.play(volume=0.1, loop=True)

    def play_select_easy(self):
        self._select_easy.play()

    def play_select_average(self):
        self._select_average.play()

    def play_select_hard(self):
        self._select_hard.play()
