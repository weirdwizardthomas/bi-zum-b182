from src.data_container.pixel import random_pixel


class Chromosome:
    def __init__(self, genotype: list, fitness_level: int):
        self.genotype = genotype  # five pixels in an image
        self.fitness_level = fitness_level

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ' fitness:' + str(self.fitness_level) + ' ' + str(self.genotype)

    def calculate_fitness(self, images: list) -> int:
        phenotype = {*()}

        for image in images:
            try:
                pixel_values = tuple(image.get_pixel_at(gene.x, gene.y) for gene in self.genotype)
                phenotype.add(pixel_values)
            except AttributeError:
                print('hi')

        return len(phenotype)

    def mutate(self, mutation, gene_probability):
        self.genotype = mutation(self.genotype, gene_probability)


def initial_chromosome(x_max: int, y_max: int, pixels_per_chromosome: int) -> Chromosome:
    pixels_per_chromosome = [random_pixel(x_max, y_max) for x in range(pixels_per_chromosome)]

    return Chromosome(pixels_per_chromosome, 0)
