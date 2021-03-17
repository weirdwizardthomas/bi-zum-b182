import heapq

from numpy import inf

from src.maze import Maze
from src.navigator.navigator import Navigator
from src.navigator.utility import node_to_coordinates, euclidean_distance


class AStar(Navigator):
    """
    An algorithm that utilises A*

    Heuristic: cost to arrive at a given vertex + euclidean distance to finish. Lower values are better.

    Attributes
    ----------

    distances: dict
        A dictionary of all vertices and their distances to finish (cost)
    end_coordinates: tuple
        A tuple of finish coordinates
    open: list
        A list of nodes on which a heap operates

    """

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.distances = {str(x): inf for x in self.maze.vertices}
        self.end_coordinates = node_to_coordinates(str(self.maze.end))
        self.open = []  # collection type is algorithm-dependent

    def open_node(self, node):
        self.__relax_edge(node)  # determine whether there's a shorter path
        distance = euclidean_distance(node_to_coordinates(node), self.end_coordinates)
        heapq.heappush(self.open, (distance + self.distances[node], node))

    def fetch_node(self):
        """
        Fetches and pops the most favourable node
        :return: Node with the best heuristic value
        """
        return heapq.heappop(self.open)[1]

    def __relax_edge(self, node):
        if node == str(self.get_start()):
            distance_to_parent = 0  # no parent for the starting point
        else:
            parent = self.path[node]
            distance_to_parent = self.distances[parent] + 1
        if self.distances[node] > distance_to_parent:
            self.distances[node] = distance_to_parent
