from numpy import random

from src.logging.logger import Logger
from src.data_container.chromosome import Chromosome
from src.config.config import Config
from src.crossover.crossover import Crossover


class UniformCrossover(Crossover):

    def cross(self, a: Chromosome, b: Chromosome) -> (Chromosome, Chromosome):
        probability = Config().data['crossover']['uniform-skew']

        genotype_1 = self.get_genotype(a, b, probability)
        genotype_2 = self.get_genotype(a, b, probability)

        c = Chromosome(genotype_1, 0)
        d = Chromosome(genotype_2, 0)

        logger = Logger(mode='Uniform crossover')
        logger.log('Parents ' + str(a) + str(b))
        logger.log('Children ' + str(c) + str(d))

        return c, d

    def get_genotype(self, a: Chromosome, b: Chromosome, probability: float) -> list:
        genotype = []
        for nucleotid in zip(a.genotype, b.genotype):
            pixel = random.choice(nucleotid, 1, p=[probability, 1 - probability])[0]
            genotype.append(pixel)
        return genotype
