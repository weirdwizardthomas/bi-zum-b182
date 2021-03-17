import argparse

from game import Game


def human_count_condition(x):
    x = int(x)
    if 0 <= x <= 2:
        return x
    else:
        raise argparse.ArgumentTypeError('Number of human players has to be between 0 and 2')


def size_condition(x):
    x = int(x)
    if x > 0:
        return x
    else:
        raise argparse.ArgumentTypeError('Board size has to be a positive non-zero number!')


parser = argparse.ArgumentParser(description='Tic-tac-toe solver')
parser.add_argument('--players', '-p', type=human_count_condition, help='Number of human players playing', default=0)
parser.add_argument('--grid-size', '-s', type=int, help='Size of the square grid', default=3)

parameters = vars(parser.parse_args())

# board init
g = Game(parameters['grid_size'], parameters['players'])
g.play()
