import arcade


class TextBox:

    def __init__(self, text, x, y, bounds_w=0, color=arcade.color.WHITE, font_size=20, is_center_aligned=False):
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
                line = current_line.strip()
                lines.append((line, arcade.get_text_image(line, self._color, self._font_size)))
                current_line = ''
                continue
            current_line += word + ' '

        if len(current_line) > 0:
            line = current_line.strip()
            lines.append((line, arcade.get_text_image(line, self._color, self._font_size)))

        return lines

    @text.setter
    def text(self, text):
        self._text = text
        self._lines = []

        if self._bounds_w > 0:
            for user_line in self._text.split('\n'):
                self._lines += self._parse_line(user_line)
        else:
            for user_line in self._text.split('\n'):
                self._lines.append((user_line, arcade.get_text_image(user_line, self._color, self._font_size)))

    def get_size(self):
        max_w = 0
        h_sum = 0
        for line, size in self._lines:
            h_sum += size.height
            max_w = max(max_w, size.width)
        return max_w, h_sum

    def on_draw(self):
        curr_y = self._y
        tb_w, _ = self.get_size()
        for line, size in self._lines:
            curr_y -= size.height

            x = self._x
            if self._is_center_aligned:
                x += tb_w / 2 - size.width / 2
            arcade.draw_text(line, x, curr_y, self._color, self._font_size)
