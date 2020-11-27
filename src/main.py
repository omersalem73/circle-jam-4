import cocos

from budget import Budget
from rating import Rating


class QuestionAndOptions(cocos.menu.Menu):

    def __init__(self):
        super().__init__()
        items = [
            cocos.menu.MenuItem("What is the bla bla bla?", self.on_new_game()),
            cocos.menu.MenuItem("1. Option A", self.on_new_game()),
            cocos.menu.MenuItem("2. Option B", self.on_new_game()),
            cocos.menu.MenuItem("3. Option C", self.on_new_game()),
            cocos.menu.MenuItem("4. Option D", self.on_new_game())
        ]
        self.menu_halign = 'left'
        self.create_menu(items)

    def on_new_game(self):
        pass

    def on_quit(self):
        pass


class GameplayInterfaceLayer(cocos.layer.Layer):

    def __init__(self):
        super().__init__()

        budget = Budget()
        rating = Rating()
        budget.set_position(10, 10)
        rating.set_position(10, 50)
        budget.add_to_renderer(self)
        rating.add_to_renderer(self)

        self.add(QuestionAndOptions())


def main():
    cocos.director.director.init(fullscreen=True)
    hello_layer = GameplayInterfaceLayer()
    color_layer = cocos.layer.ColorLayer(255, 0, 0, 255, int(cocos.director.director.get_window_size()[0] / 2), 100)
    color_layer.position = 0, 0
    main_scene = cocos.scene.Scene(hello_layer, color_layer)
    cocos.director.director.run(main_scene)


if __name__ == '__main__':
    main()
