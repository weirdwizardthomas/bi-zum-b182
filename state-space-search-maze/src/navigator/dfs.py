from queue import LifoQueue

from src.maze import Maze
from src.navigator.navigator import Navigator


class DFS(Navigator):
    """
    An algorithm that utilises DFS

    Attributes
    ----------
    open: LifoQueue
        A stack of opened nodes
    """

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.open = LifoQueue()

    def fetch_node(self):
        """
        Pops the top of the stack
        :return: Node at the top of the stack
        """
        return self.open.get()

    def open_node(self, node):
        """
        Puts a node on top of the open stack
        :return: None
        """
        self.open.put(node)  # add to stack
