from abc import abstractmethod

from src.exception.no_path_found_exception import NoPathFoundException
from src.maze import Maze


class Navigator:
    """
    A class that handles finding a path from start to finish

    Attributes
    ----------
    maze: Maze
        The maze to navigate
    edges: dict
        Edges between nodes, signifying that nodes are adjacent and traversable
    history: list
        List of all nodes visited in order
    path: dict
        Dictionary of all nodes on the found way from start to finish
    closed: set
        Set of all nodes that were visited
    open: None
        Collection specific to the algorithm used that contains nodes that were opened, but not visited yet
    """

    def __init__(self, maze: Maze):
        # data
        self.maze = maze
        self.edges = {}
        # adapt vertices for use, i.e. extract from class to key = vertex, value = neighbours
        for key in maze.vertices:
            vertex = maze.vertices[key]
            for neighbour in vertex.neighbours:
                if key not in self.edges:
                    self.edges[key] = []
                self.edges[key].append(neighbour)

        # searching collections
        self.history = []  # all visited nodes in examination order
        self.path = {}  # all nodes on the path from start to end
        self.closed = set()  # all visited nodes
        self.open = None

    def solve(self):
        """
        Finds a path from start to finish
        :raise: NoPathFoundException if no path is found from start to finish
        :return: None
        """
        # place the starting node
        self.open_node(str(self.get_start()))

        while self.open:
            # fetch current node
            current = self.fetch_node()
            # check if node has not been visited yet
            if current not in self.closed:
                # save to history
                self.__add_to_history(current)

                # check for target
                if current == str(self.__get_end()):
                    return self.__trace(), self.history
                self.__expand(current)

                # mark node as closed
                self.__close_node(current)

        raise NoPathFoundException(self.history)

    def __add_to_history(self, current):
        self.history.append(current)

    def __close_node(self, current):
        self.closed.add(current)

    def __trace(self):
        """
        Constructs a path from start to finish
        :return: Sequence of nodes from start to finish
        """
        path = []
        start = str(self.get_start())
        end = str(self.__get_end())
        while start != end:
            path.append(end)
            end = self.path[end]
        path.append(start)
        return path[::-1]

    def __expand(self, current):
        """
        Expands a node by adding all its neighbours to open nodes
        """
        neighbours = self.edges[current] if current in self.edges else []
        for neighbour in neighbours:
            if neighbour not in self.closed:
                # save parent (path)
                self.path[neighbour] = current
                # add non-visited nodes
                self.open_node(neighbour)

    def get_start(self):
        return self.maze.start

    def __get_end(self):
        return self.maze.end

    def __get_walls(self):
        return self.maze.walls.keys()

    @abstractmethod
    def open_node(self, node):
        """
        Algorithm specific way of opening a node
        """
        pass

    @abstractmethod
    def fetch_node(self):
        """
        Algorithm specific way of retrieving a node
        """
        pass


def get_solver(mode: str) -> Navigator:
    from src.navigator.bfs import BFS
    from src.navigator.dfs import DFS
    from src.navigator.random_search import RandomSearch
    from src.navigator.greedy_search import GreedySearch
    from src.navigator.dijkstra import Dijkstra
    from src.navigator.a_star import AStar

    if mode == 'BFS':
        solver = BFS
    elif mode == 'DFS':
        solver = DFS
    elif mode == 'Random':
        solver = RandomSearch
    elif mode == 'Greedy':
        solver = GreedySearch
    elif mode == 'Dijkstra':
        solver = Dijkstra
    elif mode == 'A*':
        solver = AStar
    else:
        solver = None
    return solver
