import math
import random

from src.data_container.chromosome import Chromosome
from src.data_container.pixel import random_pixel


class UnstableChromosome(Chromosome):

    def __str__(self):
        return super().__str__() + ' recognised pictures:' + str(self.fitness_level * math.sqrt(len(self.genotype)))

    def calculate_fitness(self, images: list) -> float:
        return super().calculate_fitness(images) / math.sqrt(len(self.genotype))


def initial_unstable_chromosome(x_max, y_max, pixels_count_ceiling):
    genotype_size = random.randint(1, pixels_count_ceiling)
    genotype = [random_pixel(x_max, y_max) for x in range(genotype_size)]

    return UnstableChromosome(genotype, 0)
