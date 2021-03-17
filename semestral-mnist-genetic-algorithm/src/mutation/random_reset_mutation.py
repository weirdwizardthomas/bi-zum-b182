import random

from src.data_container.chromosome import Chromosome
from src.config.config import Config
from src.logging.logger import Logger
from src.mutation.mutation import Mutation
from src.data_container.pixel import random_pixel


class RandomResetMutation(Mutation):

    def mutate(self, genotype, gene_probability):
        config = Config().data
        x_max = config['image']['width'] - 1
        y_max = config['image']['height'] - 1
        resets = config['mutation']['resets']

        logger = Logger(mode='Random reset mutation')
        logger.log('Number of genes reset ' + str(resets))
        logger.log('Original genotype ' + str(genotype))

        for x in range(resets):
            gene = random.randint(0, self.genotype_size - 1)
            genotype[gene] = random_pixel(x_max, y_max)
            logger.log('Index ' + str(gene))

        logger.log('Mutated genotype  ' + str(genotype))

        return genotype
