import math


def euclidean_distance(p: tuple, q: tuple) -> float:
    """
    Calculates euclidean distance between two vertices
    :param p: first vertex
    :param q: second vertex
    :return: Euclidean distance between the two points
    """
    a = (p[0] - q[0]) ** 2
    b = (p[1] - q[1]) ** 2
    return math.sqrt(a + b)


def node_to_coordinates(node):
    """
    Splits a node into individual coordinates
    :return: list of coordinates
    """
    return [int(x) for x in node.split(',')]
