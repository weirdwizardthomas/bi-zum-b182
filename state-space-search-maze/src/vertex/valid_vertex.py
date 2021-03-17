from src.vertex.vertex import Vertex


class ValidVertex(Vertex):
    """
    Wrapper class for vertices that can be traversed ( are not terrain)

    Attributes
    ----------

    neighbours: list
               A list of (up to 4) adjacent Valid vertices

    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.neighbours = []

    def add_neighbour(self, neighbour: Vertex):
        self.neighbours.append(str(neighbour))
