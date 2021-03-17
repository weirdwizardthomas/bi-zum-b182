from collections import deque

from src.maze import Maze
from src.navigator.navigator import Navigator


class BFS(Navigator):
    """
    An algorithm that utilises BFS

    Attributes
    ----------
    open: deque
        A queue of nodes to visit
    """

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.open = deque()

    def fetch_node(self):
        """
        Fetches & pops the front of the queue
        :return: Node at the front of the queue
        """
        return self.open.popleft()

    def open_node(self, node):
        """
        Appends the node to the queue
        :return: None
        """
        self.open.append(node)
