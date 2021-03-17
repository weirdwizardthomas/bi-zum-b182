import argparse

from src.config import IMPLEMENTED_ALGORITHMS

END = 'end'
START = 'start'
MODE = 'mode'
FILE = 'file'
MAZE = 'maze'
ALGORITHM = 'algorithm'
FILE_PATH = 'maze_file'


class InputParser:
    """
    Class that parses the input file & arguments to provide a Maze object

    Attributes
    ----------
    maze_raw : list
        Data read from the file without any processing
    file: str
        Path to the input file
    mode: str
        Algorithm to use to navigate the maze
    start: str
        Starting point of the navigation
    end: str
        Target point of the navigation
    """

    def __init__(self):
        arguments = self.__get_arguments()

        self.maze_raw = []
        self.file = arguments[FILE_PATH]
        self.mode = arguments[ALGORITHM]
        self.start = ""
        self.end = ""
        with open(self.file, "r") as file:
            self.__read_file(file)

    @staticmethod
    def __get_arguments() -> dict:
        """
        Parses command line arguments for maze path file & algorithm to use
        :return: None
        """
        arg_parser = argparse.ArgumentParser(description='Navigate maze.')
        arg_parser.add_argument(FILE_PATH,
                                metavar='M',
                                type=str,
                                help='Input maze file to be navigated.')
        algorithm_help = 'Specific algorithm to use for navigation. One of: ' + ', '.join(IMPLEMENTED_ALGORITHMS) + '.'
        arg_parser.add_argument(ALGORITHM,
                                metavar='A',
                                type=str,
                                choices=IMPLEMENTED_ALGORITHMS,
                                help=algorithm_help)
        return vars(arg_parser.parse_args())

    def __read_file(self, file):
        """
        Processes the input file for the maze, starting & ending point

        :param file: Path to the file to process
        :return: None
        """
        for line in file:
            line = line.rstrip('\n')
            if line.startswith('start'):  # find the start coordinates
                self.start = line.lstrip('start ')
            elif line.startswith('end'):  # find the end coordinates
                self.end = line.lstrip('end ')
            else:  # maze line
                self.maze_raw.append(line)

    def get_data(self) -> dict:
        """
        Packs all the data of the parser as a dictionary

        :return: Dictionary of self attributes
        """
        return {MAZE: self.maze_raw,
                FILE: self.file,
                MODE: self.mode,
                START: self.start,
                END: self.end}
