import random
from copy import deepcopy

from src.logging.logger import Logger
from src.data_container.chromosome import Chromosome
from src.config.config import Config
from src.crossover.crossover import Crossover


class KPointCrossover(Crossover):

    def cross(self, a: Chromosome, b: Chromosome) -> (Chromosome, Chromosome):
        c, d = deepcopy(a), deepcopy(b)

        config = Config().data
        k = config['crossover']['k']
        pixels_per_chromosome = config['pixels-per-chromosome']

        if k > pixels_per_chromosome or k < 1:
            raise ValueError

        breakpoints = self.determine_breakpoints(k)

        c, d = self.cross_genes(c, d, breakpoints)

        c.fitness_level = 0
        d.fitness_level = 0

        logger = Logger(mode='K point crossover')

        logger.log('K ' + str(k))
        logger.log('Breakpoints ' + ', '.join(str(x) for x in breakpoints))
        logger.log('Parents ' + str(a) + ' ' + str(b))
        logger.log('Children ' + str(c) + ' ' + str(d))

        return c, d

    def determine_breakpoints(self, k: int) -> list:
        genotype_max_index = Config().data['pixels-per-chromosome'] - 1

        breakpoints = set()
        while len(breakpoints) != k:
            breakpoints.add(random.randint(0, genotype_max_index))
        return list(breakpoints)

    def cross_genes(self, a: Chromosome, b: Chromosome, breakpoints: list) -> (Chromosome, Chromosome):
        previous = 0
        for i in breakpoints:
            if previous % 2 == 0:
                a.genotype[previous:i], b.genotype[previous:i] = b.genotype[previous:i], a.genotype[previous:i]
            previous = i
        if previous % 2 == 0:
            a.genotype[previous:], b.genotype[previous:] = b.genotype[previous:], a.genotype[previous:]
        return a, b
