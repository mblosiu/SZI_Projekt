import heapq
import math
import random

from PyQt5.QtCore import pyqtSlot, QTimer, pyqtSignal
from PyQt5.QtWidgets import QTableWidget

from board_items import BlankCell, RandomItem, Obstacle
from cart import Cart
from nuisances import PlankNuisance, GlassNuisance, WaterNuisance
from sections import FoodSection, TechSection, FloraSection, PaperSection, \
    ClothSection


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

    item_spawned = pyqtSignal(int, int)
    cart_moved = pyqtSignal(int, int)
    cart_picked_item_pos = pyqtSignal(int, int)
    cart_item_changed = pyqtSignal(str)

    calculated_cart_path_changed = pyqtSignal(bool)

    def __init__(self, rows, columns, board):
        super().__init__(rows, columns, board)

        self.board = board

        self.clean()

        self.cart = None
        self.current_field = BlankCell()
        self.calculated_cart_path = False
        self.overwritten_items = []
        self.cart_path = []
        self.add_cart()

        self.add_obstacles()
        self.add_nuisances()

        self.sections = []
        self.add_sections()

        self.board_items = []

        self.spawn_timer = QTimer()
        self.cart_mover_timer = QTimer()

        self.item_spawned.connect(self.calculate_cart_path)
        self.cart_moved.connect(self.move_cart_pos)
        self.cart_picked_item_pos.connect(self.remove_item)
        self.cart_item_changed.connect(self.board.set_item_info)

    def cart_coordinates(self):
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

        self.cart = Cart()
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
                generated_nuisance = None

                if rand_type == 0:
                    generated_nuisance = GlassNuisance()
                elif rand_type == 1:
                    generated_nuisance = PlankNuisance()
                elif rand_type == 2:
                    generated_nuisance = WaterNuisance()

                self.setItem(x, y, generated_nuisance)

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

    # TODO ?
    def clean_board_items(self):
        for el in self.board_items:
            if isinstance(self.item(el[0], el[1]), BlankCell):
                self.board_items.remove(el)

    @pyqtSlot()
    def spawn_item(self):
        rand = random.randrange(self.columnCount())

        if self.is_blank(0, rand):
            y = random.randrange(self.columnCount())
            random_item = RandomItem()
            self.setItem(0, y, random_item)
            self.board_items.append(random_item)
            self.item_spawned.emit(0, y)

    @pyqtSlot(int, int)
    def move_cart_pos(self, x, y):

        cart_x = self.cart.row()
        cart_y = self.cart.column()

        if x - cart_x == 1 and y - cart_y == 0:
            self.cart.setIcon(self.cart.backward_icon)
        if x - cart_x == -1 and y - cart_y == 0:
            self.cart.setIcon(self.cart.forward_icon)
        if x - cart_x == 0 and y - cart_y == 1:
            self.cart.setIcon(self.cart.rightward_icon)
        if x - cart_x == 0 and y - cart_y == -1:
            self.cart.setIcon(self.cart.leftward_icon)
        self.takeItem(self.cart.row(), self.cart.column())
        self.setItem(cart_x, cart_y, self.current_field)
		
        if isinstance(self.item(x, y), GlassNuisance):
            self.current_field = GlassNuisance()
        elif isinstance(self.item(x, y), PlankNuisance):
            self.current_field = PlankNuisance()
        elif isinstance(self.item(x, y), BlankCell):
            self.current_field = BlankCell()
        else:
            self.current_field = WaterNuisance()
		
        self.setItem(x, y, self.cart)
		
        # self.takeItem(self.cart.row(), self.cart.column())
		
        # self.takeItem(self.cart.row(), self.cart.column())
        # self.setItem(cart_x, cart_y, self.current_field)


        # self.setItem(x, y, self.cart)
        # self.setItem(cart_x, cart_y, BlankCell())

    @pyqtSlot()
    def start_simulation(self):
        self.spawn_timer.timeout.connect(self.spawn_item)
        self.spawn_timer.start(1000)
        self.cart_mover_timer.timeout.connect(self.move_cart)
        self.cart_mover_timer.start(75)

    @pyqtSlot()
    def drop_cart_item(self):
        self.cart.set_item(None)

    @pyqtSlot()
    def move_cart(self):
        if len(self.cart_path) > 0:
            if self.cart_path[0] is not None:
                self.cart_moved.emit(self.cart_path[0][0], self.cart_path[0][1])
                popped_item = self.cart_path.pop(0)

                if len(self.cart_path) == 0 and not self.cart.has_item():
                    picked_item = self.board_items.pop(0)
                    # self.cart_picked_item_pos.emit(popped_item[0],
                    #                                popped_item[1])
                    self.cart.set_item(picked_item)
                    self.cart_item_changed.emit(picked_item.get_attributes())

                    rand_section = random.randrange(len(self.sections))
                    self.calculated_cart_path = False
                    self.calculate_cart_path(
                        self.sections[rand_section].row(),
                        self.sections[rand_section].column())
                    # self.calculated_cart_path = False
                elif len(self.cart_path) == 0 and self.cart.has_item():
                    self.cart.set_item(None)
                    self.cart_item_changed.emit("Brak")
                    self.calculated_cart_path = False
                    rand_item = random.randrange(len(self.board_items))
                    self.calculate_cart_path(
                        self.board_items[rand_item].row(),
                        self.board_items[rand_item].column())



        # TODO
        if len(self.cart_path) == 0:
            self.calculated_cart_path = False
            self.calculated_cart_path_changed.emit(False)

    @pyqtSlot(int, int)
    def remove_item(self, x, y):
        self.setItem(x, y, BlankCell())

    @pyqtSlot(int, int)
    def calculate_cart_path(self, x, y):
        if not self.calculated_cart_path:
            self.calculated_cart_path = True
            self.calculated_cart_path_changed.emit(True)

            route = self.astar(self.cart_coordinates(), (x, y))

            for point in route.values():
                if point is not None and point != self.cart_coordinates():
                    if self.is_passable(point[0], point[1]):
                        self.cart_path.append(point)

