import random

from src.logging.logger import Logger
from src.exception.exception import NoValidSelector
from src.data_container.generation import Generation

FITNESS_PROPORTIONATE_SELECTION = 'Fitness proportionate'
TRUNCATION_SELECTION = 'Truncation'
TOURNAMENT_SELECTION_WITH_REPLACEMENT = 'Tournament replacement'
TOURNAMENT_SELECTION_NO_REPLACEMENT = 'Tournament no replacement'
RANDOM_SELECTION = 'Random'


class Selection:
    def __init__(self):
        pass

    def select(self, generation: Generation):
        pass


def selection_switch(selection: str) -> Selection:
    from src.selection.fitness_proportionate_selection import FitnessProportionateSelection
    from src.selection.random_selection import RandomSelection
    from src.selection.tournament_selection_with_replacement import TournamentSelectionWithReplacement
    from src.selection.tournament_selection_without_replacement import TournamentSelectionNoReplacement
    from src.selection.truncation_selection import TruncationSelection

    if selection is RANDOM_SELECTION:
        mode = RandomSelection
    elif selection is TOURNAMENT_SELECTION_NO_REPLACEMENT:
        mode = TournamentSelectionNoReplacement
    elif selection is TOURNAMENT_SELECTION_WITH_REPLACEMENT:
        mode = TournamentSelectionWithReplacement
    elif selection is TRUNCATION_SELECTION:
        mode = TruncationSelection
    elif selection is FITNESS_PROPORTIONATE_SELECTION:
        mode = FitnessProportionateSelection
    else:
        raise NoValidSelector

    logger = Logger(mode='Selection')
    logger.log('Type ' + selection)

    return mode()


def get_all_selections() -> list:
    return [FITNESS_PROPORTIONATE_SELECTION, TRUNCATION_SELECTION, TOURNAMENT_SELECTION_NO_REPLACEMENT,
            RANDOM_SELECTION, ]


def get_random_selection():
    selections = get_all_selections()
    selection = random.choice(selections)
    return selection_switch(selection)
