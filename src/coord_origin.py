import cocos


class CoordOrigin:

    @staticmethod
    def flip_y(y):
        return cocos.director.director.get_window_size()[1] - y
