import json
from json import JSONDecodeError

import numpy as np
import matplotlib.pyplot as plt

from src.logging.generation_statistics import GenerationStatistics


class Grapher:

    def __init__(self, filename: str):
        self.filename = filename
        self.generations = []

    def append(self, generation_number, mean, worst, best):
        self.generations.append(GenerationStatistics(generation_number, mean, worst, best))

    def plot(self):
        x = np.arange(len(self.generations))

        means = []
        lows = []
        highs = []
        for stat in self.generations:
            means.append(stat.average)
            lows.append(stat.min)
            highs.append(stat.max)

        bar_width = 0.2
        fig, ax = plt.subplots()
        ax.bar(x - bar_width, lows, width=bar_width, color='b', align='center', label='Weakest individual')
        ax.bar(x, means, width=bar_width, color='r', align='center', label='Generation average')
        ax.bar(x + bar_width, highs, width=bar_width, color='g', align='center', label='Strongest individual')

        ax.set_ylabel('Fitness score')
        ax.set_xlabel('Generation')

        ax.set_xticks(x)

        ax.legend()

        plt.savefig('../output/graph/' + self.filename + '.png')
        plt.close(fig)

    def save_means(self):
        with open('../output/means.json', 'r') as file:
            try:
                data = json.load(file)
            except JSONDecodeError:
                data = {}

        data[self.filename] = [x.average for x in self.generations]

        with open('../output/means.json', 'w') as file:
            json.dump(data, file)
