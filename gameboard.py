import heapq
import math
import random
from collections import deque

from PyQt5.QtCore import pyqtSlot, QTimer, pyqtSignal
from PyQt5.QtWidgets import QTableWidget

from board_items import BlankCell, RandomItem, Obstacle
from cart import Cart
from nuisances import PlankNuisance, GlassNuisance, WaterNuisance
from sections import FoodSection, TechSection, FloraSection, PaperSection, \
    ClothSection
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

    def __init__(self, rows, columns, board, method):
        super().__init__(rows, columns, board)

        self.board = board

        if method == 'Drzewa decyzyjne':
            self.method = 1
            self.tree = DecisionTree()
            self.tree.getTree([])
        else:
            self.method = 0
        self.clean()

        self.item_queue = deque()
        rand_y = random.randrange(0, self.columnCount())
        self.setItem(0, rand_y, RandomItem())
        self.item_queue.append((0, rand_y))

        self.cart = Cart()
        self.cart_path = []
        self.add_cart()

        self.add_obstacles()
        self.add_nuisances()

        self.sections = []
        self.add_sections()

        self.spawn_timer = QTimer()
        self.cart_mover_timer = QTimer()

        self.picked_item.connect(self.remove_item)
        self.picked_item.connect(self.find_path)

        self.dropped_item.connect(self.put_item)
        self.dropped_item.connect(self.find_path)

        self.item_changed.connect(self.board.set_item_info)

        self.overwritten_objects = []

        # self.cellClicked.connect(self.test)

    # @pyqtSlot(int, int)
    # def test(self, x, y):
    #     print(self.item(x, y))

    item_changed = pyqtSignal(str)
    item_spawned = pyqtSignal(tuple)
    picked_item = pyqtSignal()
    dropped_item = pyqtSignal()

    def cart_pos(self):
        return self.cart.row(), self.cart.column()

    def clean(self):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                self.setItem(row, column, BlankCell())

    def is_blank(self, x, y):
        return isinstance(self.item(x, y), BlankCell)

    def is_passable(self, x, y):
        return not isinstance(self.item(x, y), Obstacle)

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
            x = random.randint(2, self.rowCount() - 3)
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
        ]

        column = 1
        for section in self.sections:
            self.setItem(self.rowCount() - 1, column, section)
            column += 4

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
    def start_simulation(self):
        self.spawn_timer.timeout.connect(self.spawn_item)
        self.spawn_timer.start(1000)
        self.cart_mover_timer.timeout.connect(self.move_cart_pos)
        self.cart_mover_timer.start(150)
        self.find_path()

    @pyqtSlot()
    def spawn_item(self):
        y = random.randrange(self.columnCount())

        if self.is_blank(0, y):
            self.setItem(0, y, RandomItem())
            self.item_queue.append((0, y))

    @pyqtSlot()
    def put_item(self):
        self.cart.set_item(None)
        self.item_changed.emit("Nic")

    @pyqtSlot()
    def move_cart_pos(self):
        if len(self.cart_path) > 0:
            cart_x, cart_y = self.cart_pos()

            item = self.takeItem(self.cart_path[0][0],
                                 self.cart_path[0][1])

            self.takeItem(cart_x, cart_y)

            self.setItem(self.cart_path[0][0], self.cart_path[0][1],
                         self.cart)

            if len(self.overwritten_objects) == 0:
                self.setItem(cart_x, cart_y, BlankCell())

            if len(self.overwritten_objects) > 0:
                self.setItem(cart_x, cart_y,
                             self.overwritten_objects.pop(0))

            self.overwritten_objects.append(item)

            self.cart_path.pop(0)

        if len(self.cart_path) == 0 and not self.cart.has_item():
            self.picked_item.emit()

        if len(self.cart_path) == 0 and self.cart.has_item():
            self.dropped_item.emit()

    @pyqtSlot()
    def remove_item(self):
        picked_item = self.item_queue.popleft()
        self.cart.set_item(self.item(picked_item[0], picked_item[1]))
        self.item_changed.emit(self.cart.get_item().get_attributes())
        self.setItem(picked_item[0], picked_item[1], BlankCell())

    @pyqtSlot()
    def find_path(self):

        if self.cart.has_item():
            random_section = random.choice(self.sections)
            x, y = random_section.row(), random_section.column()
        else:
            next_item = self.item_queue[0]
            x, y = next_item[0] + 1, next_item[1]

        route = self.astar(self.cart_pos(), (x, y))

        for point in route.values():
            if point and point != self.cart_pos():
                if self.is_passable(point[0], point[1]):
                    if (point[0], point[1]) not in self.cart_path:
                        self.cart_path.append(point)
