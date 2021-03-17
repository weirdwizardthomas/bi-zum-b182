import heapq

from src.maze import Maze
from src.navigator.navigator import Navigator
from src.navigator.utility import euclidean_distance, node_to_coordinates


class GreedySearch(Navigator):
    """
    Algorithm that utilises Greedy Search
    Heuristic : euclidean distance from the finish
    Attributes
    ----------
    open: list
        list of open nodes over which a heap operates, sorted by their distance to finish
    end_coordinates: Tuple
        A tuple of x-axis and y-axis coordinates of the destination
    """

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.open = []
        self.end_coordinates = node_to_coordinates(str(self.maze.end))

    def open_node(self, node):
        """
        Inserts the node into the sorted heap based on their distance from target
        :param node: Node to insert
        :return: None
        """
        distance = euclidean_distance(node_to_coordinates(node), self.end_coordinates)
        heapq.heappush(self.open, (distance, node))

    def fetch_node(self):
        """
        Fetches the most favourable node from the heap

        """
        return heapq.heappop(self.open)[1]
