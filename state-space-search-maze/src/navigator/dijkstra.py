import heapq

from numpy import inf

from src.maze import Maze
from src.navigator.navigator import Navigator


class Dijkstra(Navigator):
    """
    An algorithm that utilises Dijkstra

    Attributes
    ----------
    open: list
        List of nodes on which a heap operates
    distances: dict
        dictionary of distances (costs) of all vertices from target

    """

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.open = []
        self.distances = {str(x): inf for x in self.maze.vertices}

    def open_node(self, node):
        self.__relax_edge(node)
        heapq.heappush(self.open, (self.distances[node], node))

    def fetch_node(self):
        return heapq.heappop(self.open)[1]

    def __relax_edge(self, node):
        """
        Determines whether a shorter path to node exists
        """
        if node == str(self.get_start()):
            distance_to_parent = 0  # no parent for the starting point
        else:
            parent = self.path[node]
            distance_to_parent = self.distances[parent] + 1
        # try to relax the stretched edge
        if self.distances[node] > distance_to_parent:
            self.distances[node] = distance_to_parent
