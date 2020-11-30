from timer import Timer


SCALE = 0.6
SCREEN_WIDTH = int(1920 * SCALE)
SCREEN_HEIGHT = int(1080 * SCALE)

timers = []
_game = None


def create_game(g):
    global _game
    _game = g


def get_game():
    global _game
    return _game


def init_game():
    get_game().init()


def add_timer(seconds, callback):
    timers.append(Timer(seconds, callback))


def sleep_before(seconds):
    def inner(func):
        def wrapper(*args, **kwargs):
            add_timer(seconds, lambda: func(*args, **kwargs))
        return wrapper
    return inner
