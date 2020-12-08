import arcade

from label import Label
from ui_base import is_point_in_rect


class Button(Label):

    def __init__(self, text, x, y, on_click_callback, *args):
        super().__init__(text, x, y, *args)
        self._on_click_callback = on_click_callback
        self._is_hovering = False
        self._is_enabled = False

    def enable(self):
        self._is_enabled = True

    def disable(self):
        self._is_enabled = False
        self._is_hovering = False

    def on_draw(self):
        if self._is_hovering:
            w, h = self.get_size()
            arcade.draw_rectangle_filled(self.x + w / 2, self.y + h / 2, w + 14, h + 5, arcade.color.ORANGE)
        super().on_draw()

    def on_mouse_motion(self, x, y, _dx, _dy):
        if self._is_enabled:
            self._is_hovering = is_point_in_rect(x, y, self.x, self.y, self.get_size()[0], self.get_size()[1])

    def on_mouse_press(self,  _x, _y, button, _modifiers):
        if self._is_enabled and (button == arcade.MOUSE_BUTTON_LEFT) and self._is_hovering:
            self._on_click_callback()
