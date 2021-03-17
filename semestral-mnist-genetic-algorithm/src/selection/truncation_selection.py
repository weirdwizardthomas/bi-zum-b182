import operator

from src.logging.logger import Logger
from src.config.config import Config
from src.data_container.generation import Generation
from src.selection.selection import Selection
from src.util import convert_to_float


class TruncationSelection(Selection):

    def select(self, generation: Generation):
        config = Config().data
        proportion = convert_to_float(config['selection']['truncation-proportion'])

        chromosomes = sorted(generation.chromosomes, key=operator.attrgetter('fitness_level'), reverse=True)
        parent_size = round(len(chromosomes) * proportion)

        logger = Logger(mode='Truncation selection')
        logger.log('Proportion ' + str(proportion))
        logger.log('Number of parents selected' + str(parent_size))

        return chromosomes[0:parent_size:]
