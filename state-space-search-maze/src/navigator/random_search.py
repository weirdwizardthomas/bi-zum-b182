import random
from collections import deque

from src.maze import Maze
from src.navigator.navigator import Navigator


class RandomSearch(Navigator):
    """
    An algorithm that at every step picks a random node to visit

    Attributes
    ----------
    open : deque
        A heap of opened nodes

    """

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.open = deque()

    def open_node(self, node):
        self.open.append(node)

    def fetch_node(self):
        """
        Fetches and pops a random open node
        :return: A random node from open nodes
        """
        open_nodes_count = len(self.open)
        index = random.randrange(open_nodes_count)
        # swap a random node with the trailing one which is easier to remove
        self.__swap(index, -1)
        return self.open.pop()

    def __swap(self, a, b):
        """
        Swaps two items in open
        :param a: index of the first item
        :param b: index of the second item
        :return: None
        """
        dummy = self.open[a]
        self.open[a] = self.open[b]
        self.open[b] = dummy
