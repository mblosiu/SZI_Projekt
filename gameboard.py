import heapq
import heapq
import math
import pprint
import random
from collections import deque

from PyQt5.QtCore import pyqtSlot, QTimer, pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from ID3 import DecisionTree
from GeneticAlgorithm import GeneticAlgorithm
from board_objects import BlankCell, RandomItem, Obstacle, TechSection, \
    FoodSection, FloraSection, PaperSection, ClothSection, \
    MedicineSection, ToySection, GlassNuisance, PlankNuisance, \
    WaterNuisance, Cart


class PQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return math.sqrt(pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2))


class GameBoard(QTableWidget):

    def set(self, coordinates: tuple, obj: QTableWidgetItem):
        self.setItem(coordinates[0], coordinates[1], obj)

    def __randomize_place(self, obj: QTableWidgetItem,
                          min_row: int = 0, max_row: int = 0,
                          min_col: int = 0, max_col: int = 0):
        rows = self.rowCount()
        cols = self.columnCount()

        if not min_row:
            min_row = 2
        if not max_row:
            max_row = rows
        if not min_col:
            min_col = 0
        if not max_col:
            max_col = cols

        coordinates = (random.randrange(min_row, max_row),
                       random.randrange(min_col, max_col))

        while not self.blank(coordinates):
            coordinates = (random.randrange(min_row, max_row),
                           random.randrange(min_col, max_col))

        self.set(coordinates, obj)

    def __setup(self, cart: tuple = None, obstacles: int = random.randrange(30),
                nuisances: int = random.randrange(30)):

        rows = self.rowCount()
        cols = self.columnCount()

        [self.set((row, col), BlankCell())
         for row in range(rows)
         for col in range(cols)]

        if not cart:
            cart = (random.randrange(5, rows), random.randrange(cols))

        self.set(cart, self.cart)

        for section in self.sections:
            self.__randomize_place(section)

        [self.__randomize_place(Obstacle()) for _ in range(obstacles)]

        for i in range(nuisances):
            rand = random.randrange(3) % 3

            if rand == 0:
                self.__randomize_place(GlassNuisance())
            elif rand == 1:
                self.__randomize_place(WaterNuisance())
            else:
                self.__randomize_place(PlankNuisance())

        y = random.randrange(cols)
        rand = RandomItem()
        self.set((0, y), rand)
        self.item_queue.append(rand)

    def get(self, coordinates: tuple) -> QTableWidgetItem:
        return self.item(coordinates[0], coordinates[1])

    def take(self, coordinates: tuple) -> QTableWidgetItem:
        return self.takeItem(coordinates[0], coordinates[1])

    def blank(self, coordinates: tuple) -> bool:
        return isinstance(self.item(coordinates[0], coordinates[1]), BlankCell)

    def passable(self, coordinates: tuple) -> bool:
        return not isinstance(self.get(coordinates), Obstacle)
        # return isinstance(item, BlankCell) or isinstance(item, Nuisance)

    def in_bounds(self, coordinates: tuple) -> bool:
        x, y = coordinates
        return 0 <= x < self.rowCount() and 0 <= y < self.columnCount()

    def __init__(self, rows: int, columns: int, board, method):
        super().__init__(rows, columns, board)

        self.board = board
        self.cart = Cart()
        self.palette_sections = []

        self.queueIndex = 0
        
        self.sections = [
            TechSection(),
            FoodSection(),
            FloraSection(),
            PaperSection(),
            ClothSection(),
            MedicineSection(),
            ToySection()
        ]

        self.item_queue = deque()

        self.__setup()

        #if method == 'Drzewa decyzyjne':
        self.method = 1
        self.tree = DecisionTree()
        self.tree.getTree([])

        self.cart_path = []
        self.cart_directions = []
        self.sections_to_visit = []
        self.overwritten_objects = []

        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_item)
        self.spawn_timer.start(100)

        self.cart_timer = QTimer()
        self.cart_timer.timeout.connect(self.move_cart_pos)
        self.cart_timer.start(150)

        self.cart_items_changed.connect(self.board.update_items_info)

        self.ga_info_changed.connect(self.board.update_ga_info)

        self.cart_stopped.connect(self.find_path)
        self.cart_stopped.emit()

    cart_stopped = pyqtSignal()
    cart_items_changed = pyqtSignal(str)
    ga_info_changed = pyqtSignal(str)

    def spawn_item(self):
        rand = random.randint(0, self.columnCount())

        if self.blank((0, rand)):
            random_item = RandomItem()
            self.set((0, rand), random_item)
            self.item_queue.append(random_item)

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
                    priority = new_cost + heuristic(goal_coordinates, next_item)
                    frontier.put(next_item, priority)
                    came_from[next_item] = current

        return came_from

    def neighbors(self, coordinates: tuple) -> list:
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        results = []

        for direction in directions:
            neighbor = (coordinates[0] + direction[0],
                        coordinates[1] + direction[1])

            results.append(neighbor)

        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return list(results)

    @pyqtSlot()
    def move_cart_pos(self):

        if len(self.cart_directions) > 0:

            if self.cart.change_direction(self.cart_directions[0]):
                return

            cart_x, cart_y = self.cart.pos()
            next_x = 0
            next_y = 0

            if self.cart_directions[0] == 'u':
                next_x, next_y = cart_x - 1, cart_y
            if self.cart_directions[0] == 'd':
                next_x, next_y = cart_x + 1, cart_y
            if self.cart_directions[0] == 'l':
                next_x, next_y = cart_x, cart_y - 1
            if self.cart_directions[0] == 'r':
                next_x, next_y = cart_x, cart_y + 1

            item = self.take((next_x, next_y))

            self.take((cart_x, cart_y))

            self.set((next_x, next_y), self.cart)

            coordinates = (cart_x, cart_y)

            if len(self.overwritten_objects) == 0:
                self.set(coordinates, BlankCell())
            else:
                self.set(coordinates, self.overwritten_objects.pop(0))

            self.overwritten_objects.append(item)

            self.cart_path.pop(0)
            self.cart_directions.pop(0)

            if len(self.cart_path) == 0:
                if not self.cart.transports_items:
                    # picked_item = self.item_queue.popleft()
                    picked_item = self.item_queue[self.queueIndex]
                    del self.item_queue[self.queueIndex]

                    self.cart.add(picked_item)
                    self.set(picked_item.pos(), BlankCell())

                    if self.cart.full():
                        self.cart.transports_items = True
                        self.cart.transports_items = True

                else:
                    # TODO Zostawianie dobrego przedmiotu
                    actual_type = self.cart.palette_sections[0]
                    to_delete = []
                    for i, el in reversed(list(enumerate(self.cart.palette))):
                        # print(i)
                        # print(i, self.cart.palette_sections[i], actual_type)
                        if self.cart.palette_sections[i] == actual_type:
                            # self.cart.palette.pop(i)
                            to_delete.append(i)
                            # self.cart.palette_sections.pop(i)
                    # self.cart.palette.pop(0)
                    # print(to_delete)
                    for el in to_delete:
                        self.cart.palette.pop(el)
                        self.cart.palette_sections.pop(el)
                    self.sections_to_visit.pop(0)
                    # self.cart.palette_sections.pop(0)
                    if len(self.sections_to_visit) == 0:
                        self.cart.transports_items = False

                self.cart_items_changed.emit(str(self.cart))
                self.cart_stopped.emit()


    def next_item_generator(self):
        next_item = self.item_queue[0].pos()
        newIndex = 0
        while math.fabs(self.cart.pos()[1] - next_item[1]) < 4 and math.fabs(self.cart.pos()[0] - next_item[0] < 2):
            newIndex = random.randint(0, len(self.item_queue))
            print(newIndex)
            next_item = self.item_queue[newIndex].pos()
        self.queueIndex = newIndex
        return next_item
            
                
    @pyqtSlot()
    def find_path(self):

        # Zbieraj przedmioty
        if not self.cart.full() and not self.cart.transports_items:
            # next_item = self.item_queue[0].pos()
            print(len(self.item_queue))
            next_item = self.next_item_generator()
            
            # next_item = self.item_queue[random.randint(0, len(self.item_queue))].pos()
            # print('cartpos')
            # print(self.cart.pos()[1])
            # print('cartpos')
            x, y = next_item[0] + 1, next_item[1]

            route = self.astar(self.cart.pos(), (x, y))
            # pprint.pprint('przedmiot')
            # pprint.pprint((x, y))
            # pprint.pprint(len(route))
            # pprint.pprint(route.values())

            # self.cart_path = list(route.values())
            for point in route.values():
                if point and point != self.cart.pos():
                    if self.passable(point):
                        if (point[0], point[1]) not in self.cart_path:
                            self.cart_path.append(point)
            # print(self.cart_path)

            cart_x, cart_y = self.cart.pos()

            for i in range(len(self.cart_path)):
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

        # Odstaw przedmioty
        if self.cart.transports_items:
            # TODO Drzewo przekazuje sekcje
            # print(self.tree.predict([self.cart.palette[0].hardness, self.cart.palette[0].weight, self.cart.palette[0].size, self.cart.palette[0].shape, self.cart.palette[0].condensation, self.cart.palette[0].przeznaczenie]))
            if len(self.sections_to_visit) == 0:
                # sections = random.sample(self.sections, len(self.sections))
                sections = []
                for el in self.cart.palette:
                    type = self.tree.predict([el.hardness, el.weight, el.size, el.shape, el.condensation, el.przeznaczenie])
                    
                    if type == 'RTV':
                        typeSecition = self.sections[0]
                    elif type == 'Zywnosc':
                        typeSecition = self.sections[1]
                    elif type == 'Ogrodnictwo':
                        typeSecition = self.sections[2]
                    elif type == 'Art. Pap.':
                        typeSecition = self.sections[3]
                    elif type == 'odziez':
                        typeSecition = self.sections[4]
                    elif type == 'Leki':
                        typeSecition = self.sections[5]
                    else:
                        typeSecition = self.sections[6]
                    self.cart.palette_sections.append(type)
                    if typeSecition not in sections:
                        sections.append(typeSecition)
                # print(sections)
                for section in sections:
                    self.sections_to_visit.append(section.pos())
                # print(self.sections_to_visit)
                ga = GeneticAlgorithm(self.sections_to_visit)
                self.ga_info_changed.emit(str(ga))
                self.sections_to_visit = ga.path

            # FIXME POWTARZANIE KODU
            next_section = self.sections_to_visit[0]
            x, y = next_section[0], next_section[1]

            route = self.astar(self.cart.pos(), (x, y))

            for point in route.values():
                if point and point != self.cart.pos():
                    if self.passable(point):
                        if (point[0], point[1]) not in self.cart_path:
                            self.cart_path.append(point)

            cart_x, cart_y = self.cart.pos()

            for i in range(len(self.cart_path)):
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
