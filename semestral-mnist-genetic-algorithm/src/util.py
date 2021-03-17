import json
import random
import matplotlib.pyplot as plt
import numpy as np


def convert_to_float(frac_str: str) -> float:
    # https://stackoverflow.com/questions/1806278/convert-fraction-to-float
    try:
        return float(frac_str)
    except ValueError:
        numerator, denominator = frac_str.split('/')
        try:
            leading, numerator = numerator.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(numerator) / float(denominator)
        return whole - frac if whole < 0 else whole + frac


def decision(probability: float) -> bool:
    """
    Evalutes an event given a probability
    :param probability: Probability of the event, from interval <0,1>
    :return: True if the event happened, False otherwise
    """
    return random.random() < probability


def compile_graph(input_file: str, output_file: str, keyword: str):
    """
    Graphs all data containing in an input json file into a single graph
    :param input_file: File to read data from
    :param output_file: File to write the graph to
    :param keyword: Keyword that marks data to graph
    :return: None
    """
    with open(input_file, 'r') as file:
        data = json.load(file)

    fig, ax = plt.subplots(figsize=(10, 5))
    x = []

    for method, y in data.items():
        if keyword in method:
            x = np.arange(len(y))
            ax.plot(x, y, '-o', label=method)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    ax.set_xlabel('Generation')
    ax.set_ylabel('Fitness')

    ax.set_xticks(x)

    plt.savefig('../output/graph/' + keyword + '.png', bbox_inches='tight')
