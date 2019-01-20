import math
import random
from pprint import pprint


def distance(first_point: tuple, second_point: tuple):
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

        for i in range(1, len(self.points)):
            first_point = self.points[i]

            second_point = self.points[i - 1]
            # if i + 1 == len(self.points):
            #     second_point = self.points[0]
            # else:
            #     second_point = self.points[i + 1]

            self.fitness += distance(first_point, second_point)


class Population:

    def __init__(self, list_of_point_lists: list, size: int,
                 mutation_rate: int = 0.01):

        self.routes = []
        self.size = size
        self.mutation_rate = mutation_rate

        self.overall_fitness = 0
        for points in list_of_point_lists:
            route = Route(points)
            self.routes.append(route)
            self.overall_fitness += route.fitness

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

        self.parents = set()
        # Ruletka
        # while len(self.parents) < size // 2:
        #     rand = random.randrange(0, round(self.overall_fitness))
        #     val = self.overall_fitness
        #
        #     for route in self.routes:
        #         val -= route.fitness
        #         if val < rand:
        #             self.parents.add(route)
        #             break

        #Turniej
        while len(self.parents) < size // 2:
            k = random.sample(self.routes, random.randint(2, len(self.routes)))
            best = min(k, key=lambda x: x.fitness)

            self.parents.add(best)

            # if best not in self.parents:
            #     self.parents.append(best)

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

    def __init__(self, points: list, generations: int = 100,
                 population_size: int = 100, stop: int = 15):

        initial_population = []
        while len(initial_population) != population_size:
            initial_population.append(random.sample(points, len(points)))

        population = Population(initial_population, population_size)
        # print(f"Początkowy koszt: {population.start_distance}")

        self.initial_cost = population.start_distance

        init_cost = population.start_distance
        no_change = 0

        for generation in range(generations):
            population = Population(population.breed(), population_size)

            if population.start_distance == init_cost:
                no_change += 1
            else:
                init_cost = population.start_distance
                no_change = 0

            if no_change == stop:
                break

            # print(f"Generacja {generation}: {population.start_distance}")

        # print(f"Końcowy koszt: {population.start_distance}")

        self.final_cost = population.start_distance

        # print(f"Trasa {population.shortest().points}")

        self.path = population.shortest().points

    def __str__(self):
        s = f"Początkowy koszt: {round(self.initial_cost, 2)}\n"
        s += f"Końcowy koszt: {round(self.final_cost, 2)}\n"
        s += "Trasa:\n"
        for point in self.path:
            s += f"{point}\n"
        return s


if __name__ == "__main__":
    # print(distance((-1, 1), (3, 4)))
    sections = [(2, 16), (4, 7), (19, 3), (3, 3), (15, 0), (17, 5)]
    # initial = []
    # while len(initial) != 100:
    #     initial.append(random.sample(secs, len(secs)))

    gen = GeneticAlgorithm(sections)

    # pop = Population(initial, 100)
    # for r in pop.routes:
    #     print(r.points)
    #     print(r.fitness)
    # pprint(pop.routes.points)
