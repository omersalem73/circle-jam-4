import cocos


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


class HelloWorld(cocos.layer.Layer):

    def __init__(self):
        super().__init__()
        budget = cocos.text.Label(
            'Budget: $150,000',
            font_name='Times New Roman',
            font_size=24,
            anchor_y='top'
        )
        w, h = cocos.director.director.get_window_size()
        budget.position = 10, h - 10
        self.add(budget)

        rating = cocos.text.Label(
            'Rating: 12.2%',
            font_name='Times New Roman',
            font_size=24,
            anchor_y='top'
        )
        rating.position = 10, h - 50
        self.add(rating)
        self.add(QuestionAndOptions())


def main():
    cocos.director.director.init(fullscreen=True)
    hello_layer = HelloWorld()
    main_scene = cocos.scene.Scene(hello_layer)
    cocos.director.director.run(main_scene)


if __name__ == '__main__':
    main()
