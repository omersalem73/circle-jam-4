import arcade

from button import Button
from globals import get_game


class SoundController:

    def __init__(self):
        self._theme = arcade.sound.Sound('sound/theme.wav')
        self._select_easy = arcade.sound.Sound('sound/select_easy.wav')
        self._select_average = arcade.sound.Sound('sound/select_average.wav')
        self._select_hard = arcade.sound.Sound('sound/select_hard.wav')
        self._mute_button = Button('Mute', 20, 10, on_click_callback=self._toggle_mute)
        self._theme_sound = None
        self._is_muted = False

        get_game().register('on_draw', self._mute_button.on_draw)
        get_game().register_button_mouse_events(self._mute_button)

    @property
    def mute_button(self):
        return self._mute_button

    def _toggle_mute(self):
        self._is_muted = not self._is_muted

        if self._is_muted:
            self._mute_button.text = 'Unmute'
            if self._theme_sound:
                arcade.sound.stop_sound(self._theme_sound)
        else:
            self._mute_button.text = 'Mute'
            self.play_theme_in_loop()

    def play_theme_in_loop(self):
        self._theme_sound = self._theme.play(volume=0.1, loop=True)

    def play_select_easy(self):
        if not self._is_muted:
            self._select_easy.play()

    def play_select_average(self):
        if not self._is_muted:
            self._select_average.play()

    def play_select_hard(self):
        if not self._is_muted:
            self._select_hard.play()
