import matplotlib.pyplot as plt
import numpy as np


class GenerationStatistics:
    def __init__(self, generation_number: int, average_fitness: float, min_fitness: int, max_fitness: int):
        self.generation_number = generation_number
        self.average = average_fitness
        self.min = min_fitness
        self.max = max_fitness
