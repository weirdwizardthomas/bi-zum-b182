from src.input_parser import MAZE, START, END
from src.vertex.valid_vertex import ValidVertex
from src.vertex.vertex import Vertex, adapt_vertex

WALL = 'X'


class Maze:
    """
    Class that represents the maze to navigate

    Attributes
    ----------
    width : int
            width of the maze
    height : int
            height of the maze
    start : Vertex
            Starting point in the maze
    end : Vertex
            Target point in the maze

    canvas : List
            A matrix containing all the text representation of the maze

    vertices: dict
            Collection of traversable vertices

    walls : dict
            Collection of wall pertices
    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.start = Vertex(0, 0)
        self.end = Vertex(0, 0)
        self.canvas = []
        self.vertices = {}
        self.walls = {}


class Builder:
    def __init__(self, data: dict):
        self.width = len(data[MAZE][0])
        self.height = len(data[MAZE])
        self.start = data[START]
        self.end = data[END]
        self.canvas = data[MAZE]

    def build(self) -> Maze:
        maze = Maze()
        maze.width = self.width
        maze.height = self.height
        maze.start = adapt_vertex(self.start)
        maze.end = adapt_vertex(self.end)
        maze.canvas = self.canvas
        maze.vertices, maze.walls = self.__adapt_maze()
        return maze

    def __adapt_maze(self):
        """
        Parses the canvas for walls and traversable vertices
        :return: a tuple of a list of traversable vertices and a list of impassable vertices
        """
        width = len(self.canvas[0])
        height = len(self.canvas)
        vertices = {}
        walls = {}

        for row in range(height):
            for column in range(width):
                vertex_value = self.canvas[row][column]

                if vertex_value is WALL:
                    vertex = Vertex(row, column)
                    walls[str(vertex)] = vertex
                else:
                    vertex = self.__find_neighbours(ValidVertex(row, column), column, row)
                    vertices[str(vertex)] = vertex

        return vertices, walls

    def __find_neighbours(self, vertex, column, row) -> ValidVertex:
        """
        Given a traversable vertex, finds all its traversable neighbours

        :param vertex: Vertex for which neighbours are to be found
        :param column: column in which the vertex is located
        :param row: row in wich the vertex is located
        :return: vertex with all its neighbours added
        """

        # check surrounding vertices
        neighbour_coordinates = [(row + 1, column),
                                 (row - 1, column),
                                 (row, column + 1),
                                 (row, column - 1)]
        for coordinates in neighbour_coordinates:
            x, y = coordinates
            neighbour = self.canvas[x][y]
            if neighbour is not WALL:
                vertex.add_neighbour(Vertex(x, y))
        return vertex
