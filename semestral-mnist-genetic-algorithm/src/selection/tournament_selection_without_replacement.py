import operator
import random
from copy import deepcopy

from src.logging.logger import Logger
from src.config.config import Config
from src.data_container.generation import Generation
from src.selection.selection import Selection


class TournamentSelectionNoReplacement(Selection):

    def select(self, generation: Generation):
        config = Config().data
        tournament_size = config['selection']['tournament-size']
        pool_size = config['parent-pool-size']

        contenders = self.prepare_contenders(generation.chromosomes)

        first = 0
        last = tournament_size
        size = len(contenders)

        victors = []

        while first < size and len(victors) < pool_size:
            tournament = contenders[first:last]
            victor = max(tournament, key=operator.attrgetter('fitness_level'))
            victors.append(victor)
            first = last
            last += tournament_size

        logger = Logger(mode='Tournament Selection (no replacement)')
        logger.log('Tournament size ' + str(tournament_size))
        logger.log('Pool size ' + str(pool_size))
        logger.log('Tournament rounds ' + str(last // tournament_size))
        logger.log('Selected chromosomes\n' + '\n'.join(str(x) for x in victors))

        return victors

    def prepare_contenders(self, challengers: list):
        contenders = deepcopy(challengers)
        random.shuffle(contenders)
        return contenders
