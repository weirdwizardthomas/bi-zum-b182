import random

from src.config.config import Config
from src.data_container.pixel import Pixel
from src.logging.logger import Logger
from src.mutation.mutation import Mutation
from src.util import decision

SHIFT_CHOICES = [-1, 1]


class TwoAxisShiftMutation(Mutation):

    def mutate(self, genotype, gene_probability, ):
        config = Config().data

        logger = Logger(mode='Single axis shift mutation')
        logger.log('Original genotype ' + str(genotype))
        for gene in genotype:
            if decision(gene_probability):
                gene = self.mutate_gene(gene)
        logger.log('Mutated genotype  ' + str(genotype))
        return genotype

    def mutate_gene(self, gene: Pixel) -> Pixel:
        config = Config().data

        gene.x = (gene.x + random.choice(SHIFT_CHOICES)) % config['image']['width']
        gene.y = (gene.y + random.choice(SHIFT_CHOICES)) % config['image']['height']

        return gene
