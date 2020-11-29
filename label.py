import arcade


class Label:

    def __init__(self, text, x, y, color=arcade.color.WHITE, font_size=26):
        self._image = None
        self._color = color
        self._font_size = font_size
        self.text = text
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._image = arcade.get_text_image(self._text, self._color, self._font_size)

    def get_size(self):
        return self._image.width, self._image.height

    def on_draw(self):
        arcade.draw_text(self._text, self._x, self._y, self._color, self._font_size)
