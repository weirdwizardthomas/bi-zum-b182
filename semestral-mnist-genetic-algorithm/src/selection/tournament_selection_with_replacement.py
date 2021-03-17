import operator
import random

from src.logging.logger import Logger
from src.config.config import Config
from src.data_container.generation import Generation
from src.selection.selection import Selection


class TournamentSelectionWithReplacement(Selection):

    def select(self, generation: Generation):
        config = Config().data
        tournament_size = config['selection']['tournament-size']
        pool_size = config['island-size']

        victors = set()

        while len(victors) < pool_size:
            if len(generation.chromosomes) == 0:
                input('error')
            contenders = random.sample(generation.chromosomes, tournament_size)
            victor = max(contenders, key=operator.attrgetter('fitness_level'))
            victors.add(victor)

        logger = Logger(mode='Tournament Selection (replacement)')
        logger.log('Tournament size' + str(tournament_size))
        logger.log('Pool size' + str(pool_size))
        logger.log('Tournament rounds ' + str(len(victors) // tournament_size))
        logger.log('Selected chromosomes\n' + '\n'.join(str(x) for x in victors))

        return list(victors)
