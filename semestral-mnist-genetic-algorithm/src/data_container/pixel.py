from random import randint


class Pixel:
    """
    Wrapper class for natural 2D coordinates

    Attributes
    ----------
    x : int
        x-axis coordinate in a 2D image
    y : int
        y-axis coordinate in a 2D image
    """

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '[' + str(self.x) + ',' + str(self.y) + ']'


def random_pixel(max_x: int, max_y: int) -> Pixel:
    """Generates a pixel with a random position in specified boundaries

    :param max_x: maximal x-axis coordinate
    :param max_y: maximal y-axis coordinate
    :return: Pixel object with random coordinates
    """

    return Pixel(randint(0, max_x), randint(0, max_y))
