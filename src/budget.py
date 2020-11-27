import cocos
from coord_origin import CoordOrigin


class Budget:

    def __init__(self):
        self._label = cocos.text.Label(
            'Budget: $150,000',
            font_name='Times New Roman',
            font_size=24,
            anchor_y='top'
        )

    def set_position(self, x, y):
        self._label.position = x, CoordOrigin.flip_y(y)

    def add_to_renderer(self, renderer):
        renderer.add(self._label)
