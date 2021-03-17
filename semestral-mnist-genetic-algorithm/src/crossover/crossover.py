import random

from src.exception.exception import NoValidCrosser
from src.logging.logger import Logger
from src.data_container.chromosome import Chromosome

K_POINT_CROSSOVER = 'K point'
UNIFORM_CROSSOVER = 'Uniform'


class Crossover:

    def cross(self, a: Chromosome, b: Chromosome) -> (Chromosome, Chromosome):
        pass


def crossover_switch(crossover: str) -> Crossover:
    from src.crossover.k_point_crossover import KPointCrossover
    from src.crossover.uniform_crossover import UniformCrossover

    if crossover is K_POINT_CROSSOVER:
        mode = KPointCrossover
    elif crossover is UNIFORM_CROSSOVER:
        mode = UniformCrossover
    else:
        raise NoValidCrosser

    logger = Logger(mode='Crossover')
    logger.log('Type ' + crossover)

    return mode()


def get_all_crossovers() -> list:
    return [K_POINT_CROSSOVER, UNIFORM_CROSSOVER]


def get_random_crossover():
    crossovers = get_all_crossovers()
    crossover = random.choice(crossovers)
    return crossover_switch(crossover)
