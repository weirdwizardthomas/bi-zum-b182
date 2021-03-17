import numpy as np

from src.logging.logger import Logger
from src.config.config import Config
from src.data_container.generation import Generation
from src.selection.selection import Selection


class FitnessProportionateSelection(Selection):

    def select(self, generation: Generation):
        """
        Selects a subpopulation, with individuals with a better fitness value having higher chance of being picked
        :param generation: Generation from which parents are selected
        :return: List of parents for the next generation
        """
        generation_fitness = sum(chromosome.fitness_level for chromosome in generation.chromosomes)
        proportional_fitness = [chromosome.fitness_level / generation_fitness for chromosome in
                                generation.chromosomes]

        pool_size = Config().data['parent-pool-size']
        selected_chromosomes = np.random.choice(generation.chromosomes, int(np.sqrt(pool_size)), p=proportional_fitness)

        logger = Logger(mode='Fitness proportionate selection')
        logger.log('Generation fitness ' + str(generation_fitness))
        logger.log('Pool size ' + str(pool_size))

        logger.log('Proportional fitness\n' + str(np.array(generation.chromosomes)))  # todo add chromosomes as well
        logger.log('Selected chromosomes\n' + str(selected_chromosomes))

        return selected_chromosomes
