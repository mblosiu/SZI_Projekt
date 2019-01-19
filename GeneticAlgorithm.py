import math
import random
from pprint import pprint


def distance(first_point: tuple, second_point: tuple) -> float:
    x_distance = (second_point[0] - first_point[0]) ** 2
    y_distance = (second_point[1] - first_point[1]) ** 2
    return math.sqrt(x_distance + y_distance)


def order_1(first_parent: list, second_parent: list):

    start_index = random.randrange(0, len(first_parent))
    stop_index = random.randrange(start_index, len(first_parent))

    child = [None for _ in first_parent]
    child[start_index:stop_index] = first_parent[start_index:stop_index]

    for point in second_parent:
        if point not in child:
            child[child.index(None)] = point

    return child


def crossover(first_parent: list, second_parent: list):
    return (order_1(first_parent, second_parent),
            order_1(second_parent, first_parent))


def mutate(route: list):
    first_point = random.choice(route)
    second_point = random.choice(route)

    while second_point == first_point:
        second_point = random.choice(route)

    route[route.index(first_point)] = second_point
    route[route.index(second_point)] = first_point

    return route


class Route:

    def __init__(self, points: list):
        self.fitness = 0
        self.points = points
        self.selection_probability = 0

        # print(points)
    # def calc_fitness(self):

        for i in range(len(self.points)):
            first_point = self.points[i]

            if i + 1 == len(self.points):
                second_point = self.points[0]
            else:
                second_point = self.points[i + 1]

            self.fitness += distance(first_point, second_point)


class Population:

    def __init__(self, list_of_routes: list, size: int,
                 mutation_rate: int = 0.01):

        self.routes = []
        self.size = size
        self.mutation_rate = mutation_rate

        for route in list_of_routes:
            self.routes.append(Route(route))

        self.start_distance = self.routes[0].fitness

        # self.fitness_sum = 0
        #
        # for route in self.routes:
        #     # route.calc_fitness()
        #     self.fitness_sum += route.fitness

        # for route in self.routes:
        #     route.selection_probability = route.fitness / self.fitness_sum

        # self.selection_probabilities = [route.selection_probability for route in self.routes]

        # pprint(self.selection_probabilities)

        self.parents = []

        # print(parents)
        # print(size)
        #
        # while len(parents) < (size // 2):
        #     rand, x, ind = random.random(), 1, 0
        #
        #     for selection_probability in self.selection_probabilities:
        #         x -= selection_probability
        #         if x < rand:
        #             parents.append(self.routes[ind])
        #             break
        #
        # print(parents)

        while len(self.parents) < size // 2:
            k = random.sample(self.routes, random.randint(2, len(self.routes)))
            best = min(k, key=lambda x: x.fitness)

            if best not in self.parents:
                self.parents.append(best)

        # print(self.parents)
        # print(len(self.parents))
        # for p in self.parents:
        #     print(p.selection_probability)

    # def selection(self, k: int = random.sample(self.routes)):
    #     chance = random.randrange(self.fitness_sum)

    # def tournament(self, count: int = ):

    def breed(self):
        new_routes = []

        while len(new_routes) < self.size:
            parents = random.sample(self.parents, 2)
            children = crossover(parents[0].points, parents[1].points)

            if random.random() <= self.mutation_rate:
                children = (mutate(children[0]), mutate(children[1]))

            new_routes.append(children[0])
            new_routes.append(children[1])

        return new_routes

    def shortest(self):
        fitness = [route.fitness for route in self.routes]
        return self.routes[fitness.index(min(fitness))]


class GeneticAlgorithm:

    def __init__(self, points: list, generations: int = 300,
                 population_size: int = 100):

        initial_population = []
        while len(initial_population) != population_size:
            initial_population.append(random.sample(points, len(points)))

        population = Population(initial_population, population_size)
        # print(f"Początkowy koszt: {population.start_distance}")

        self.initial_cost = population.start_distance

        for generation in range(0, generations):
            population = Population(population.breed(), population_size)
            print(f"Generacja {generation}: {population.start_distance}")
            # print(population.fitness_sum)

        # print(f"Końcowy koszt: {population.start_distance}")

        self.final_cost = population.start_distance

        # print(f"Trasa {population.shortest().points}")

        self.path = population.shortest().points

    def __str__(self):
        return f"""Początkowy koszt: {round(self.initial_cost, 2)}\nKońcowy koszt: {round(self.final_cost, 2)}\nTrasa: {self.path}"""


if __name__ == "__main__":
    # print(distance((-1, 1), (3, 4)))
    secs = [(2, 16), (4, 7), (19, 3), (3, 3), (15, 0), (17, 5)]
    initial = []
    while len(initial) != 100:
        initial.append(random.sample(secs, len(secs)))

    gen = GeneticAlgorithm(initial)
    # pop = Population(initial, 100)
    # for r in pop.routes:
    #     print(r.points)
    #     print(r.fitness)
    # pprint(pop.routes.points)
