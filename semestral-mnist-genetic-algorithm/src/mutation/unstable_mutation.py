import random

from src.config.config import Config
from src.data_container.pixel import Pixel, random_pixel
from src.mutation.mutation import Mutation
from src.util import decision

SHIFT_CHOICES = [-1, 1]


class UnstableMutation(Mutation):
    def mutate(self, genotype, gene_probability):
        # try to mutate number of pixels
        config = Config().data

        original_size = len(genotype)
        mutated_size = original_size
        if decision(gene_probability):
            bound = config['mutation']['genotype-size-change']
            mutated_size = max(1, original_size + random.randint(-bound, bound))  # adjust so the size is not negative

        self.fit_to_size(config, genotype, mutated_size, original_size)
        for gene in genotype:
            if decision(gene_probability):
                gene = self.mutate_gene(gene)

        return genotype

    def fit_to_size(self, config, genotype, mutated_size, original_size):
        if original_size > mutated_size:  # chromosome mutated into a shorter one, need to remove at random
            random.shuffle(genotype)
            while len(genotype) > mutated_size:
                genotype.pop()
        elif original_size < mutated_size:  # chromosome mutated into a longer one, need to add new ones
            x_max = config['image']['width'] - 1
            y_max = config['image']['height'] - 1

            while len(genotype) < mutated_size:
                genotype.append(random_pixel(x_max, y_max))

    def mutate_gene(self, gene: Pixel) -> Pixel:
        config = Config().data

        gene.x = (gene.x + random.choice(SHIFT_CHOICES)) % config['image']['width']
        gene.y = (gene.y + random.choice(SHIFT_CHOICES)) % config['image']['height']
        return gene
