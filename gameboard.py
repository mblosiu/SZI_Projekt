import enum
import heapq
import json
import math
import random
from collections import deque
from pprint import pprint

from PyQt5.QtCore import pyqtSlot, QTimer, pyqtSignal, QSize
from PyQt5.QtWidgets import QTableWidget

from GeneticAlgorithm import GeneticAlgorithm

from board_objects import BlankCell, RandomItem, Obstacle, CategorizedItem, \
    TechSection, FoodSection, FloraSection, PaperSection, ClothSection, \
    MedicineSection, ToySection, Section, GlassNuisance, PlankNuisance, \
    WaterNuisance, Nuisance
from cart import Cart
from DecisionTree import DecisionTree


class PQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class GameBoard(QTableWidget):

    item_changed = pyqtSignal(str)
    item_spawned = pyqtSignal(tuple)
    picked_item = pyqtSignal()
    dropped_item = pyqtSignal()
    go_to_section = pyqtSignal()
    ga_info_changed = pyqtSignal(str)

    def __init__(self, rows: int, columns: int, board, method):
        super().__init__(rows, columns, board)

        self.board = board

        if method == 'Drzewa decyzyjne':
            self.method = 1
            self.tree = DecisionTree()
            self.tree.getTree([])

        self.clean()

        self.item_queue = deque()
        rand_y = random.randrange(0, self.columnCount())
        self.setItem(0, rand_y, RandomItem())
        self.item_queue.append((0, rand_y))

        self.cart_path = []
        self.cart_directions = []

        self.cart = Cart()
        self.add_cart()

        self.sections = []
        self.add_sections()

        self.add_obstacles()
        self.add_nuisances()

        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_item)

        self.cart_mover_timer = QTimer()
        self.cart_mover_timer.timeout.connect(self.move_cart_pos)

        self.picked_item.connect(self.remove_item)
        self.picked_item.connect(self.find_path)

        self.dropped_item.connect(self.put_item)
        self.dropped_item.connect(self.find_path)

        self.item_changed.connect(self.board.update_items_info)
        self.ga_info_changed.connect(self.board.update_ga_info)

        self.go_to_section.connect(self.find_path)

        # if self.method == 2:
        #
        #     data = None
        #     with open("ga_dataset.json") as f:
        #         data = json.load(f)
        #
        #     while not self.cart.full_capacity():
        #         for d in data:
        #             x = CategorizedItem(d)
        #             self.cart.add_item(x)
        #
        #     self.item_changed.emit(str(self.cart))
        #     self.dropped_item.emit()

        self.overwritten_objects = []

    @pyqtSlot()
    def start_simulation(self):
        self.spawn_timer.start(100)
        self.cart_mover_timer.start(150)
        self.find_path()

    def cart_pos(self):
        return self.cart.row(), self.cart.column()

    def section_pos(self, index):
        return self.sections[index].row(), self.sections[index].column()

    def clean(self):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                self.setItem(row, column, BlankCell())

    def is_blank(self, x, y):
        return isinstance(self.item(x, y), BlankCell)

    def is_passable(self, x, y):
        item = self.item(x, y)
        return not isinstance(item, Obstacle)
        # return isinstance(item, BlankCell) or isinstance(item, Nuisance)

    def add_cart(self, x=None, y=None):
        if x is None:
            x = random.randrange(1, self.rowCount() - 1)
        if y is None:
            y = random.randrange(0, self.columnCount())

        self.setItem(x, y, self.cart)

    def add_obstacles(self, count=random.randint(0, 30)):
        for i in range(count):
            x = random.randint(2, self.rowCount() - 3)
            y = random.randint(0, self.columnCount())

            if self.is_blank(x, y):
                self.setItem(x, y, Obstacle())

    def add_nuisances(self, count=random.randint(10, 50)):
        nuisances = 3

        for i in range(count):
            x = random.randint(2, self.rowCount())
            y = random.randint(0, self.columnCount())

            if self.is_blank(x, y):
                rand_type = random.randrange(nuisances)

                if rand_type == 0:
                    self.setItem(x, y, GlassNuisance())
                elif rand_type == 1:
                    self.setItem(x, y, PlankNuisance())
                elif rand_type == 2:
                    self.setItem(x, y, WaterNuisance())

    def add_sections(self):

        self.sections = [
            TechSection(),
            FoodSection(),
            FloraSection(),
            PaperSection(),
            ClothSection(),
            MedicineSection(),
            ToySection()
        ]

        for section in self.sections:
            x = random.randint(2, self.rowCount())
            y = random.randint(0, self.columnCount())

            while not self.is_blank(x, y):
                x = random.randint(2, self.rowCount())
                y = random.randint(0, self.columnCount())

            self.setItem(x, y, section)

    def astar(self, start_coordinates: tuple, goal_coordinates: tuple):

        frontier = PQueue()
        frontier.put(start_coordinates, 0)
        came_from = {start_coordinates: None}
        cost_so_far = {start_coordinates: 0}

        while not frontier.empty():
            current = frontier.get()

            if current == goal_coordinates:
                break

            for next_item in self.neighbors(current):
                new_cost = cost_so_far[current] - 1

                if next_item not in cost_so_far \
                        or new_cost > cost_so_far[next_item]:
                    cost_so_far[next_item] = new_cost
                    priority = new_cost + self.heuristic(goal_coordinates,
                                                         next_item)
                    frontier.put(next_item, priority)
                    came_from[next_item] = current

        return came_from

    def neighbors(self, coordinates: tuple):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        result = []

        for direction in directions:
            neighbor = (coordinates[0] + direction[0],
                        coordinates[1] + direction[1])

            if 0 <= neighbor[0] <= self.rowCount() and \
                    0 <= neighbor[1] <= self.columnCount():

                if self.is_passable(neighbor[0], neighbor[1]):
                    result.append(neighbor)

        return result

    @staticmethod
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return math.sqrt(pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2))

    @pyqtSlot()
    def spawn_item(self):
        y = random.randrange(self.columnCount())

        if self.is_blank(0, y):
            self.setItem(0, y, RandomItem())
            self.item_queue.append((0, y))

    @pyqtSlot()
    def put_item(self):
        self.item_changed.emit(str(self.cart))

    @pyqtSlot()
    def move_cart_pos(self):
        if len(self.cart_directions) > 0:
            cart_x, cart_y = self.cart_pos()

            if self.cart_directions[0] == 'u':
                next_x, next_y = cart_x - 1, cart_y
            if self.cart_directions[0] == 'd':
                next_x, next_y = cart_x + 1, cart_y
            if self.cart_directions[0] == 'l':
                next_x, next_y = cart_x, cart_y - 1
            if self.cart_directions[0] == 'r':
                next_x, next_y = cart_x, cart_y + 1

            item = self.takeItem(next_x, next_y)

            self.takeItem(cart_x, cart_y)

            self.setItem(next_x, next_y, self.cart)

            if len(self.overwritten_objects) == 0:
                self.setItem(cart_x, cart_y, BlankCell())

            if len(self.overwritten_objects) > 0:
                self.setItem(cart_x, cart_y, self.overwritten_objects.pop(0))

            self.overwritten_objects.append(item)

            self.cart_path.pop(0)
            self.cart_directions.pop(0)

            if len(self.cart_directions) == 0:
                self.picked_item.emit()
            #
            # if len(self.cart_directions) == 0 and self.cart.has_item():
            #     self.dropped_item.emit()

    @pyqtSlot()
    def remove_item(self):
        picked_item = self.item_queue.popleft()
        self.cart.add_item(self.item(picked_item[0], picked_item[1]))
        self.setItem(picked_item[0], picked_item[1], BlankCell())
        self.item_changed.emit(str(self.cart))
    
    @pyqtSlot()
    def find_path(self):

        if not self.cart.full_capacity() and not self.cart.transports_items:
            next_item = self.item_queue[0]
            x, y = next_item[0] + 1, next_item[1]

            route = self.astar(self.cart_pos(), (x, y))

            for point in route.values():
                if point and point != self.cart_pos():
                    if self.is_passable(point[0], point[1]):
                        if (point[0], point[1]) not in self.cart_path:
                            self.cart_path.append(point)

            cart_x, cart_y = self.cart_pos()

            for i in range(0, len(self.cart_path)):
                if i == 0:
                    if cart_x > self.cart_path[i][0]:
                        self.cart_directions.append('u')
                    elif cart_x < self.cart_path[i][0]:
                        self.cart_directions.append('d')
                    elif cart_y > self.cart_path[i][1]:
                        self.cart_directions.append('l')
                    elif cart_y < self.cart_path[i][1]:
                        self.cart_directions.append('r')
                else:
                    if self.cart_path[i-1][0] > self.cart_path[i][0]:
                        self.cart_directions.append('u')
                    elif self.cart_path[i-1][0] < self.cart_path[i][0]:
                        self.cart_directions.append('d')
                    elif self.cart_path[i-1][1] > self.cart_path[i][1]:
                        self.cart_directions.append('l')
                    elif self.cart_path[i-1][1] < self.cart_path[i][1]:
                        self.cart_directions.append('r')

        elif self.cart.full_capacity() and not self.cart.transports_items:
            self.cart.transports_items = True

        # TODO Połączenie z drzewem/siecią
        if self.cart.transports_items:
            # self.ga_info_changed.emit("Obliczanie drogi..")
            if len(self.cart.sections_to_go) == 0:
                sections = random.sample(self.sections,
                                         len(self.sections))

                for sec in sections:
                    self.cart.sections_to_go.append((sec.row(), sec.column()))

                ga = GeneticAlgorithm(self.cart.sections_to_go)
                self.ga_info_changed.emit(str(ga))
                self.cart.sections_to_go = ga.path
                self.go_to_section.emit()

            else:
                next_section = self.cart.sections_to_go.pop(0)

                route = self.astar(self.cart_pos(), (next_section[0],
                                                     next_section[1]))

                for point in route.values():
                    if point and point != self.cart_pos():
                        if self.is_passable(point[0], point[1]):
                            if (point[0], point[1]) not in self.cart_path:
                                self.cart_path.append(point)

                cart_x, cart_y = self.cart_pos()

                for i in range(0, len(self.cart_path)):
                    if i == 0:
                        if cart_x > self.cart_path[i][0]:
                            self.cart_directions.append('u')
                        elif cart_x < self.cart_path[i][0]:
                            self.cart_directions.append('d')
                        elif cart_y > self.cart_path[i][1]:
                            self.cart_directions.append('l')
                        elif cart_y < self.cart_path[i][1]:
                            self.cart_directions.append('r')
                    else:
                        if self.cart_path[i - 1][0] > self.cart_path[i][0]:
                            self.cart_directions.append('u')
                        elif self.cart_path[i - 1][0] < self.cart_path[i][0]:
                            self.cart_directions.append('d')
                        elif self.cart_path[i - 1][1] > self.cart_path[i][1]:
                            self.cart_directions.append('l')
                        elif self.cart_path[i - 1][1] < self.cart_path[i][1]:
                            self.cart_directions.append('r')

                if len(self.cart.sections_to_go) == 0:
                    self.cart.transports_items = False
                    # TODO
                    self.cart.palette = []



        # if self.method == 1:
        #     # print(self.cart.get_item().size)
        #     attr = [self.cart.get_item(len(self.cart.palette)).hardness, self.cart.get_item(len(self.cart.palette)).weight, self.cart.get_item(len(self.cart.palette)).size,
        #             self.cart.get_item(len(self.cart.palette)).shape, self.cart.get_item(len(self.cart.palette)).condensation]
        #     type = self.tree.predict(attr)
        #     self.item_changed.emit(type)
        #     print(type)
        #     if type == 'RTV':
        #         section = self.sections[0]
        #     elif type == 'Zywnosc':
        #         section = self.sections[1]
        #     elif type == 'Ogrodnictwo':
        #         section = self.sections[2]
        #     elif type == 'Art. Pap.':
        #         section = self.sections[3]
        #     elif type == 'odziez':
        #         section = self.sections[4]
        #     else:
        #         random_section = random.choice(self.sections)
        #
        #     x, y = section.row(), section.column()
        # else:
        #     random_section = random.choice(self.sections)
        #     x, y = random_section.row(), random_section.column()


        # if self.cart.full_capacity() or self.method == 2:
        #
        #     points = set()
        #     # points.add(self.cart_pos())
        #
        #     for item in self.cart.palette:
        #         section_type = item.attributes["typ"]
        #
        #         if section_type == "RTV":
        #             points.add(self.section_pos(0))
        #         elif section_type == "Zywnosc":
        #             points.add(self.section_pos(1))
        #         elif section_type == "Ogrodnictwo":
        #             points.add(self.section_pos(2))
        #         elif section_type == "Art. Pap.":
        #             points.add(self.section_pos(3))
        #         elif section_type == "Odziez":
        #             points.add(self.section_pos(4))
        #
        #     print(points)
        #     # gen = GeneticAlgorithm.GeneticAlgorithm(list(points))
        #     return
        #
        # if not self.cart.full_capacity():
        #     next_item = self.item_queue[0]
        #     x, y = next_item[0] + 1, next_item[1]

        # if self.cart.has_item():
        #     if self.method == 1:
        #         # print(self.cart.get_item().size)
        #         attr = [self.cart.get_item(len(self.cart.palette)).hardness, self.cart.get_item(len(self.cart.palette)).weight, self.cart.get_item(len(self.cart.palette)).size,
        #                 self.cart.get_item(len(self.cart.palette)).shape, self.cart.get_item(len(self.cart.palette)).condensation]
        #         type = self.tree.predict(attr)
        #         self.item_changed.emit(type)
        #         print(type)
        #         if type == 'RTV':
        #             section = self.sections[0]
        #         elif type == 'Zywnosc':
        #             section = self.sections[1]
        #         elif type == 'Ogrodnictwo':
        #             section = self.sections[2]
        #         elif type == 'Art. Pap.':
        #             section = self.sections[3]
        #         elif type == 'odziez':
        #             section = self.sections[4]
        #         else:
        #             random_section = random.choice(self.sections)
        #         x, y = section.row(), section.column()
        #     else:
        #         random_section = random.choice(self.sections)
        #         x, y = random_section.row(), random_section.column()
        # else:
        #     next_item = self.item_queue[0]
        #     x, y = next_item[0] + 1, next_item[1]

        # route = self.astar(self.cart_pos(), (x, y))
        #
        # for point in route.values():
        #     if point and point != self.cart_pos():
        #         if self.is_passable(point[0], point[1]):
        #             if (point[0], point[1]) not in self.cart_path:
        #                 self.cart_path.append(point)
        #
        # cart_x, cart_y = self.cart_pos()
        # for i in range(0, len(self.cart_path)):
        #     if i == 0:
        #         if cart_x > self.cart_path[i][0]:
        #             self.cart_directions.append('u')
        #         elif cart_x < self.cart_path[i][0]:
        #             self.cart_directions.append('d')
        #         elif cart_y > self.cart_path[i][1]:
        #             self.cart_directions.append('l')
        #         elif cart_y < self.cart_path[i][1]:
        #             self.cart_directions.append('r')
        #     else:
        #         if self.cart_path[i-1][0] > self.cart_path[i][0]:
        #             self.cart_directions.append('u')
        #         elif self.cart_path[i-1][0] < self.cart_path[i][0]:
        #             self.cart_directions.append('d')
        #         elif self.cart_path[i-1][1] > self.cart_path[i][1]:
        #             self.cart_directions.append('l')
        #         elif self.cart_path[i-1][1] < self.cart_path[i][1]:
        #             self.cart_directions.append('r')
