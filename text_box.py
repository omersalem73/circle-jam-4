import arcade


class TextBox:

    def __init__(self, text, bounds_w, x, y, color=arcade.color.WHITE, font_size=20):
        self._text = None
        self._lines = None
        self._bounds_w = bounds_w
        self._x = x
        self._y = y
        self._color = color
        self._font_size = font_size
        self.text = text

    @property
    def text(self):
        return self._text

    def _parse_line(self, line):
        words = line.split(' ')
        lines = []
        current_line = ''

        for word in words:
            if arcade.get_text_image(current_line + word, self._color, self._font_size).width > self._bounds_w:
                lines.append(current_line.strip())
                current_line = ''
                continue
            current_line += word + ' '

        if len(current_line) > 0:
            lines.append(current_line.strip())

        return lines

    @text.setter
    def text(self, text):
        self._text = text
        self._lines = []
        for user_line in self._text.split('\n'):
            self._lines += self._parse_line(user_line)

    def on_draw(self):
        curr_y = self._y
        for line in self._lines:
            curr_y -= arcade.get_text_image(line, self._color, self._font_size).height
            arcade.draw_text(line, self._x, curr_y, self._color, self._font_size)
