import random
from operator import attrgetter

import numpy as np

from src.data_container.chromosome import initial_chromosome
from src.config.config import Config
from src.data_container.unstable_chromosome import initial_unstable_chromosome, UnstableChromosome
from src.util import decision


class Generation:
    """Holder of a population of chromosomes that represent a single generation

    """

    def __init__(self, chromosomes: list):
        self.chromosomes: list = chromosomes

    def __str__(self):
        return '\n'.join([str(x) for x in self.chromosomes])

    def calculate_fitness(self, images: list):
        for chromosome in self.chromosomes:
            chromosome.fitness_level = chromosome.calculate_fitness(images)

    def mean(self):
        return np.mean([chromosome.fitness_level for chromosome in self.chromosomes])

    def worst(self):
        return min(self.chromosomes, key=attrgetter('fitness_level')).fitness_level

    def best(self):
        return max(self.chromosomes, key=attrgetter('fitness_level')).fitness_level

    def mutate(self, mutator, gene_probability, genotype_probability):
        mutants = []
        for chromosome in self.chromosomes:
            if decision(genotype_probability):
                chromosome.mutate(mutator, gene_probability)
            mutants.append(chromosome)

        self.chromosomes = mutants

    def get_subgeneration(self, start, stop):
        subgeneration = self.chromosomes[start:stop]
        del (self.chromosomes[start:stop])

        return subgeneration

    def toss_a_stone(self, logger):
        # pick
        config = Config().data
        survivor_proportion = config['cataclysm']['survivors']
        survivor_count = int(survivor_proportion * len(self.chromosomes))
        self.chromosomes = random.sample(self.chromosomes, survivor_count)
        logger.log('Cataclysm!' + str(survivor_proportion * 100) + " % of the population has been wiped out!")

        is_unstable = type(self.chromosomes[0]) == UnstableChromosome
        new_chromosomes_size = config['island-size'] - len(self.chromosomes)
        new_chromosomes = unstable_chromosomes(new_chromosomes_size) if is_unstable else stable_chromosomes(
            new_chromosomes_size)
        self.chromosomes += new_chromosomes

    def lost_diversity(self) -> bool:
        config = Config().data
        unique_combinations = set(tuple(x.genotype) for x in self.chromosomes)

        print("Diversity", len(unique_combinations))
        return len(unique_combinations) / len(self.chromosomes) < config['cataclysm']['uniques']


def breed(parents, pool_size, crosser, single_offspring=False):
    children = []
    i = 0
    while len(children) < pool_size:
        mum, dad = parents[i], parents[(i + 1) % len(parents)]
        if not single_offspring:
            boy, girl = crosser(mum, dad)

            children.append(boy)
            children.append(girl)
        else:
            offspring = crosser(mum, dad)
            children.append(offspring)
        i = (i + 1) % len(parents)  # breed circularly

    return children


def stable_chromosomes(population_size: int):
    config = Config().data
    x_max = config['image']['width'] - 1
    y_max = config['image']['height'] - 1
    pixels_per_chromosome = config['pixels-per-chromosome']

    return [initial_chromosome(x_max, y_max, pixels_per_chromosome) for x in range(population_size)]


def unstable_chromosomes(population_size: int):
    config = Config().data
    x_max = config['image']['width'] - 1
    y_max = config['image']['height'] - 1
    pixel_count_ceiling = config['pixels-count-max']

    return [initial_unstable_chromosome(x_max, y_max, pixel_count_ceiling) for x in range(population_size)]


def initial_generation(population_size: int) -> Generation:
    return Generation(stable_chromosomes(population_size))


def initial_unstable_generation(population_size: int) -> Generation:
    return Generation(unstable_chromosomes(population_size))
