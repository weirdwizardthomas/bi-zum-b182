import argparse
import datetime

from src.config.config import Config
from src.crossover.crossover import get_random_crossover
from src.crossover.unstable_uniform_crossover import UnstableUniformCrossover
from src.data_container.letter_image import load_letters
from src.island import initialise_island, migrate
from src.logging.logger import Logger
from src.mutation.mutation import get_random_mutation
from src.mutation.unstable_mutation import UnstableMutation
from src.selection.selection import get_random_selection, selection_switch, TOURNAMENT_SELECTION_NO_REPLACEMENT


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Genetic algorithm for finding unique pixels across images in a dataset')
    parser.add_argument('--islands', '-i', type=int, help='Number of islands of the population', default=1)
    parser.add_argument('--population', '-p', type=int, help='Generation size', default=500)
    parser.add_argument('--stable', '-s', type=str, help='Stable for static genotype size, Unstable for dynamic',
                        default='stable')
    args = vars(parser.parse_args())
    island_count = args['islands']
    config['generation-size'] = args['population']
    config['island-size'] = config['generation-size'] // island_count
    config['parent-pool-size'] = config['island-size'] // 4

    return args


config = Config().data
logger = Logger(str(datetime.datetime.now()))

args = parse_arguments()

if args['stable'] == 'stable':
    input_data = load_letters('latin-dataset')
    islands = {island_index:
                   initialise_island(config['island-size'],
                                     get_random_selection().select,
                                     get_random_crossover().cross,
                                     get_random_mutation().mutate,
                                     island_index,
                                     input_data,
                                     logger,
                                     False)
               for island_index in range(args['islands'])}
elif args['stable'] == 'unstable':
    input_data = load_letters('hiragana-dataset')
    islands = {island_index:
                   initialise_island(config['island-size'],
                                     get_random_selection().select,
                                     UnstableUniformCrossover().cross,
                                     UnstableMutation().mutate,
                                     island_index,
                                     input_data,
                                     logger,
                                     True)
               for island_index in range(args['islands'])}
else:
    raise argparse.ArgumentTypeError("Not one of 'unstable' or 'stable' ")

for i in range(config['number-of-generations']):
    for island in islands.values():
        island.run_one_cycle(i, input_data)

    if i % 3 == 0:
        migrate(islands, 0.2, logger)
