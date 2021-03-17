import random

from src.data_container.chromosome import Chromosome
from src.config.config import Config
from src.exception.exception import NoValidMutator
from src.logging.logger import Logger

RANDOM_RESET_MUTATION = 'Random reset'
SINGLE_AXIS_SHIFT_MUTATION = 'Single axis shift'
TWO_AXIS_SHIFT_MUTATION = 'Two axis shift'


class Mutation:
    def __init__(self):
        self.genotype_size = Config().data['pixels-per-chromosome']

    def mutate(self, genotype, gene_probability):
        pass


def mutation_switch(mutation: str) -> Mutation:
    from src.mutation.random_reset_mutation import RandomResetMutation
    from src.mutation.single_axis_shift_mutation import SingleAxisShiftMutation
    from src.mutation.two_axis_shift_mutation import TwoAxisShiftMutation

    if mutation is RANDOM_RESET_MUTATION:
        mode = RandomResetMutation
    elif mutation is SINGLE_AXIS_SHIFT_MUTATION:
        mode = SingleAxisShiftMutation
    elif mutation is TWO_AXIS_SHIFT_MUTATION:
        mode = TwoAxisShiftMutation
    else:
        raise NoValidMutator

    logger = Logger(mode='Mutation')
    logger.log('Type ' + mutation)

    return mode()


def get_all_mutations() -> list:
    return [RANDOM_RESET_MUTATION, SINGLE_AXIS_SHIFT_MUTATION, TWO_AXIS_SHIFT_MUTATION]


def get_random_mutation():
    mutations = get_all_mutations()
    mutation = random.choice(mutations)
    return mutation_switch(mutation)
