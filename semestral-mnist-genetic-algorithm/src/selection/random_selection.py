import random

from src.logging.logger import Logger
from src.config.config import Config
from src.data_container.generation import Generation
from src.selection.selection import Selection


class RandomSelection(Selection):

    def select(self, generation: Generation):
        """
        Selects parents for the next generation by picking individuals at random
        :param generation:
        :return:
        """
        pool_size = Config().data['parent-pool-size']
        selected_chromosomes = random.sample(generation.chromosomes, pool_size)

        logger = Logger(mode='Random selection')
        logger.log('Pool size ' + str(pool_size))
        logger.log('Selected chromosomes\n' + '\n'.join(str(x) for x in selected_chromosomes))

        return selected_chromosomes
