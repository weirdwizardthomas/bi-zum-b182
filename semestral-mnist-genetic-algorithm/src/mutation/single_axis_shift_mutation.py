import random

from src.config.config import Config
from src.data_container.pixel import Pixel
from src.logging.logger import Logger
from src.mutation.mutation import Mutation
from src.util import decision

X_AXIS = 'x'
Y_AXIS = 'y'


class SingleAxisShiftMutation(Mutation):

    def mutate(self, genotype, gene_probability):
        axis = random.choice([X_AXIS, Y_AXIS])
        shift = random.choice([-1, 1])

        logger = Logger(mode='Single axis shift mutation')
        logger.log('Shifted axis ' + axis)
        logger.log('Shift ' + str(shift))
        logger.log('Original genotype ' + str(genotype))

        for gene in genotype:
            if decision(gene_probability):
                gene = self.mutate_gene(gene, axis, shift)

        logger.log('Mutated genotype  ' + str(genotype))

        return genotype

    def mutate_gene(self, gene: Pixel, axis: str, shift: int) -> Pixel:
        config = Config().data

        if axis is X_AXIS:
            gene.x = (gene.x + shift) % config['image']['width']
        if axis is Y_AXIS:
            gene.y = (gene.y + shift) % config['image']['height']

        return gene
