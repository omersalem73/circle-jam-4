import arcade


class TextBox:

    def __init__(self, text, bounds_w, x, y, color=arcade.color.WHITE, font_size=20, is_center_aligned=False):
        self._text = None
        self._lines = None
        self._bounds_w = bounds_w
        self._x = x
        self._y = y
        self._color = color
        self._font_size = font_size
        self._is_center_aligned = is_center_aligned
        self.text = text

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

    def get_size(self):
        max_w = 0
        h_sum = 0
        for line in self._lines:
            h_sum += arcade.get_text_image(line, self._color, self._font_size).height
            max_w = max(max_w, arcade.get_text_image(line, self._color, self._font_size).width)
        return max_w, h_sum

    def on_draw(self):
        curr_y = self._y
        tb_w, _ = self.get_size()
        for line in self._lines:
            line_size = arcade.get_text_image(line, self._color, self._font_size)
            curr_y -= line_size.height

            x = self._x
            if self._is_center_aligned:
                x += tb_w / 2 - line_size.width / 2
            arcade.draw_text(line, x, curr_y, self._color, self._font_size)
