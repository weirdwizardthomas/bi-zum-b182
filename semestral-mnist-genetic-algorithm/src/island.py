import random
from math import ceil

from src.config.config import Config
from src.data_container.generation import initial_generation, breed, initial_unstable_generation


class Island:
    def __init__(self, generation, selector, crosser, mutator, gene_mutation_probability, genotype_mutation_probability,
                 island_number, logger, is_unstable=False):
        self.generation = generation
        self.gene_mutation_probability = gene_mutation_probability
        self.genotype_mutation_probability = genotype_mutation_probability
        self.mutator = mutator
        self.crosser = crosser
        self.selector = selector
        self.island_number = island_number
        self.is_unstable = is_unstable

        self.logger = logger
        self.logger.log('Genotype mutation probability ' + str(self.genotype_mutation_probability))
        self.logger.log('Gene mutation probability ' + str(self.gene_mutation_probability))
        self.logger.log('Stochastic generation:' + str(self.generation))

    def run_one_cycle(self, generation_number, input_data):
        config = Config().data

        if self.generation.lost_diversity():
            self.generation.toss_a_stone(self.logger)
            self.generation.calculate_fitness(input_data)

        parents = self.selector(self.generation)

        self.generation.chromosomes = breed(parents, config['island-size'], self.crosser, self.is_unstable)
        self.generation.mutate(self.mutator, self.gene_mutation_probability, self.genotype_mutation_probability)
        self.generation.calculate_fitness(input_data)

        self.logger.mode = 'Island' + str(self.island_number)
        self.logger.log('Generation number [' + str(generation_number) + ']\n' + str(self.generation))

    def emigrate(self, flock_proportion: float):
        flock_size = ceil(flock_proportion * len(self.generation.chromosomes))
        start = random.randint(0, len(self.generation.chromosomes) - flock_size - 1)
        flock = self.generation.get_subgeneration(start, start + flock_size)
        self.logger.log('Emigrating ' + str(flock) + " : " + str(flock))
        return flock

    def immigrate(self, flock):
        self.logger.log('Immigrating ' + str(len(flock)) + " : " + str(flock))
        self.generation.chromosomes += flock


def initialise_island(size: int, selector, crosser, mutator, i: int, input_data, logger, is_unstable=False) -> Island:
    generation = initial_generation(size) if not is_unstable else initial_unstable_generation(size)
    generation.calculate_fitness(input_data)

    gene_mutation_probability = random.uniform(0, 0.5)
    genotype_mutation_probability = random.uniform(0, 0.5)

    config = Config().data

    return Island(generation, selector, crosser, mutator, gene_mutation_probability, genotype_mutation_probability, i,
                  logger, is_unstable)


def migrate(islands, flock_proportion, logger):
    if len(islands) == 1:
        return

    flocks = {island.island_number: island.emigrate(flock_proportion) for island in islands.values()}

    island_count = len(islands)
    migration_paths = get_migration_permutations(island_count)
    logger.log('Migration paths: ' + str(migration_paths))
    for source, target in migration_paths.items():
        flock = flocks.pop(source)
        islands[target].immigrate(flock)


def check_permutation(permutation):
    for i in range(len(permutation)):
        if i == permutation[i]:
            return False
    return True


def get_migration_permutations(island_count: int) -> dict:
    permutation = [*range(island_count)]

    while not check_permutation(permutation):
        random.shuffle(permutation)

    return {i: permutation[i] for i in range(len(permutation))}
