import arcade

class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()


def main():
    game = Game(600, 400, 'My Game')
    arcade.run()


if __name__ == '__main__':
    main()
