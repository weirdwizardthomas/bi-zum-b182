class Vertex:
    """
    Wrapper class representing a vertex in a 2-D plane, with x-axis and y-axis coordinates

    Attributes
    ----------
    x : int
        x-axis coordinate in a 2-D plane
    y : int
        y-axis coordinate ina 2-D plane
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ',' + str(self.y)


def adapt_vertex(coordinates: str) -> Vertex:
    """Converts a string into coordinates

    :param coordinates: String to parse for coordinates
    :return : Vertex with x & equal to input coordinates
    """
    y, x = coordinates.split(",")
    return Vertex(int(x), int(y))
