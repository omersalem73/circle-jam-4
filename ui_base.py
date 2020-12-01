class CallbacksRegisterer:

    def __init__(self):
        self._callbacks = {
            'on_draw': [],
            'on_mouse_press': [],
            'on_mouse_motion': []
        }

    def register(self, name, callback):
        self._callbacks[name].append(callback)

    def on_draw(self):
        for callback in self._callbacks['on_draw']:
            callback()

    def on_mouse_press(self, *args):
        for callback in self._callbacks['on_mouse_press']:
            callback(*args)

    def on_mouse_motion(self, *args):
        for callback in self._callbacks['on_mouse_motion']:
            callback(*args)


class VisibilityToggle:

    def __init__(self):
        self._is_visible = True

    @property
    def is_visible(self):
        return self._is_visible

    def hide(self):
        self._is_visible = False

    def show(self):
        self._is_visible = True
        self.on_draw()

    def draw_if_visible(self):
        raise NotImplemented

    def on_draw(self):
        if not self.is_visible:
            return
        return self.draw_if_visible()


def is_point_in_rect(x, y, rx, ry, rw, rh):
    return (x >= rx) and (x <= rx + rw) and (y >= ry) and (y <= ry + rh)
