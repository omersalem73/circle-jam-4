import cocos
from coord_origin import CoordOrigin


class Rating:

    def __init__(self):
        self._label = cocos.text.Label(
            'Rating: 12.7%',
            font_name='Times New Roman',
            font_size=24,
            anchor_y='top'
        )

    def set_position(self, x, y):
        self._label.position = x, CoordOrigin.flip_y(y)

    def add_to_renderer(self, renderer):
        renderer.add(self._label)
