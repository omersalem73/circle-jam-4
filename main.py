import arcade
from game import Game
from globals import create_game, init_game


def main():
    create_game(Game())
    init_game()
    arcade.run()


if __name__ == '__main__':
    main()
