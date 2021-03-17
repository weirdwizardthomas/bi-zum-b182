import os

import numpy as np
from PIL import Image

from src.config.config import Config


class LetterImage:
    """Holder of data related to an image of a letter


    Attributes
    ----------
    image_pixels: array
        2D matrix of pixels of the image
    letter: str
        A single character that is depicted in the image
    """

    def __init__(self, image_folder: str, image_name: str):
        # load a letter image and convert it to rgb
        image = Image.open(image_folder + image_name)
        # store pixels
        self.image_pixels = np.array(image)
        self.letter = image_name.strip('.bmp').capitalize()

    def get_pixel_at(self, x: int, y: int) -> tuple:
        """ Gets a single pixel from the image specified by its x-axis and y-axis coordinates

        :param x: x-axis coordinate of the pixel
        :param y: y-axis coordinate of the pixel
        :todo change return: True if pixel at [x][y] is black, False if white
        """

        pixel = self.image_pixels[x][y]
        if type(pixel) == np.uint8:
            pixel = [pixel, pixel, pixel]

        return tuple(pixel)


def load_letters(key):
    """ Loads all images from a folder

    :return: list of LetterImage
    """
    config = Config().data
    training_data_directory = config['path'][key]

    return [LetterImage(training_data_directory, x) for x in os.listdir(training_data_directory)]
