from random import random

from src.crossover.crossover import Crossover
from src.data_container.chromosome import Chromosome
from src.data_container.unstable_chromosome import UnstableChromosome
from src.util import decision


class UnstableUniformCrossover(Crossover):

    def cross(self, a: UnstableChromosome, b: UnstableChromosome) -> UnstableChromosome:
        pool = {x for x in (a.genotype + b.genotype)}
        genotype = []
        probability = 0.5

        while len(genotype) < min(len(a.genotype), len(b.genotype)):
            for gene in pool:
                if decision(probability):
                    genotype.append(gene)

        return UnstableChromosome(genotype, 0)
