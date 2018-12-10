import heapq
import math
import random

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, \
    QTableWidgetItem, QTableWidget

from board_items import BlankCell, Obstacle, RandomItem, PathCell
from cart import astar
from nuisances import GlassNuisance, PlankNuisance
from sections import FloraSection, PaperSection, ClothSection, FoodSection, \
    TechSection


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
    cart_moved = pyqtSignal(int, int, QTableWidgetItem)
    cart_picked_item = pyqtSignal()
    cart_picked_item_pos = pyqtSignal(int, int)
    cart_dropped_item = pyqtSignal()

    def clean(self):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                self.setItem(row, column, BlankCell())

    def __init__(self, rows, columns, board):
        super().__init__(rows, columns, board)

        self.board = board

        self.clean()

        cart_x = random.randrange(1, self.rowCount() - 1)
        cart_y = random.randrange(self.columnCount())
        self.cart = Cart(self)

        self.setItem(cart_x, cart_y, self.cart)

        # self.cart = Cart(random.randrange(1, self.rowCount() - 1),
        #                  random.randrange(self.columnCount()), self)
        # self.setItem()
        # self.add_cart()
        self.add_obstacles()
        self.add_nuisances()
        self.sections = []
        self.add_sections()

        self.board_items = []

        self.spawn_timer = QTimer()
        self.cart_mover_timer = QTimer()

        # self.cart_picked_item.connect(self.board.set_item_info)
        # self.cart_dropped_item.connect(self.board.set_item_info)
        # self.cart_picked_item_pos.connect(self.remove_item)
        # self.cart_moved.connect(self.move_cart)

    def is_blank(self, x, y):
        return isinstance(self.item(x, y), BlankCell)

    def is_passable(self, x, y):
        return not isinstance(self.item(x, y), Obstacle)
    # def add_cart(self):
    #     self.setItem(random.randrange(1, self.rowCount() - 1),
    #                  random.randrange(self.columnCount()), Cart(self))

    def add_obstacles(self, count=random.randint(0, 30)):
        for i in range(count):
            x = random.randint(2, self.rowCount() - 3)
            y = random.randint(0, self.columnCount())

            if self.is_blank(x, y):
                self.setItem(x, y, Obstacle())

    def add_nuisances(self, count=random.randint(10, 50)):

        nuisances = 2

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
                    priority = new_cost + self.heuristic(goal_coordinates, next_item)
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

    @pyqtSlot(int, int)
    def remove_item(self, x, y):
        self.setItem(x, y, BlankCell())
        self.board_items.remove((x, y))

    @pyqtSlot()
    def spawn_item(self):
        rand = random.randrange(self.columnCount())

        if self.is_blank(0, rand):
            y = random.randrange(self.columnCount())
            self.setItem(0, y, RandomItem())
            self.board_items.append((0, y))
            self.item_spawned.emit(0, y)

    @pyqtSlot(int, int, QTableWidgetItem)
    def move_cart(self, x, y, cart):
        cart_x = cart.row()
        cart_y = cart.column()
        self.takeItem(cart.row(), cart.column())
        self.setItem(x, y, cart)
        self.setItem(cart_x, cart_y, BlankCell())

    @pyqtSlot()
    def start_simulation(self):
        self.spawn_timer.timeout.connect(self.spawn_item)
        self.spawn_timer.start(1000)
        # self.cart_mover_timer.start(100)
        self.cart.move_timer.start(100)


class Cart(QTableWidgetItem):

    def is_route_calculated(self):
        return self.route_calculated

    def calc_route(self, x, y):
        if self.is_route_calculated() is False:
            self.route_calculated = True
            route = astar((self.row(), self.column()), (x + 1, y), self.table)

            for i in route.values():
                if i is not None:
                    if i != (self.row(), self.column()) and i != (x + 1, y):
                        if self.table.is_blank(i[0], i[1]):
                            self.path.append(i)
                            self.table.setItem(i[0], i[1], PathCell())

    # TODO
    class Palette:
        def __init__(self, capacity: int, items: list):
            self.capacity = capacity
            self.items = items

    def __init__(self, table: GameBoard):
        super().__init__()

        self.setIcon(QIcon("images/forklift.svg"))
        self.table = table
        self.route_calculated = False
        self.palette = self.Palette(1, [])
        self.path = []
        self.goal_coords = None
        self.item = None
        self.table.item_spawned.connect(self.calc_route)
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_cart)

    def move_cart(self):
        if len(self.path) > 0:
            if self.path[0] is not None:
                self.table.cart_moved.emit(self.path[0][0], self.path[0][1],
                                           self)
                self.path.pop(0)

                if len(self.path) == 0:
                    if self.item is None:
                        self.item = 1
                        self.palette.items.append("Przedmiot 1")
                        # self.table.cart_picked_item_pos.emit(
                        #     self.goal_coords[0] - 1, self.goal_coords[1])
                        # self.table.cart_picked_item.emit()
                    else:
                        self.item = None
                        self.palette.items.pop(0)
                        # self.table.cart_dropped_item.emit()

                    # Przenieś przedmiot do sekcji
                    if self.item == 1:
                        random_section_number = random.randrange(5)
                        route = astar(
                            (self.row(), self.column()),
                            (self.table.sections[random_section_number].row(),
                            self.table.sections[random_section_number].column()), self.table)
                        for i in route.values():
                            if i is not None:
                                if i != (self.row(), self.column()) and i != (self.table.sections[random_section_number].row(),
                            self.table.sections[random_section_number].column()):
                                    if self.table.is_blank(i[0], i[1]):
                                        self.path.append(i)
                                        self.table.setItem(i[0], i[1],
                                                           PathCell())
                    # Idź po przedmiot
                    else:
                        random_item = random.randrange(len(self.table.board_items))
                        random_item = self.table.board_items[random_item]
                        route = astar((self.row(), self.column()), (random_item[0] + 1, random_item[1]),
                                      self.table)
                        for i in route.values():
                            if i is not None:
                                if i != (self.row(), self.column()) and i != (random_item[0] + 1, random_item[1]):
                                    if self.table.is_blank(i[0], i[1]):
                                        self.path.append(i)
                                        self.table.setItem(i[0], i[1],
                                                           PathCell())



class BoardWindow(QWidget):

    teaching_method_changed = pyqtSignal(int)

    def __init__(self, method):
        super().__init__()
        self.resize(1366, 866)
        self.setLayout(self.init_ui(method))
        self.show()
        self.teaching_method = None

    def init_ui(self, method):
        main_layout = QVBoxLayout()

        font = QFont("Sans", 12)

        name = QLabel(f"Agent: Wózek widłowy, Metoda: {method}")
        name.setFont(font)
        name.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(name)

        # TODO
        cart_items = QLabel(f"Przedmiot wózka: ")
        cart_items.setFont(font)
        cart_items.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(cart_items)

        table = GameBoard(20, 20, self)

        for i in range(table.columnCount()):
            table.setColumnWidth(i, 65)

        main_layout.addWidget(table)

        self.teaching_method_changed.connect(table.start_simulation)

        return main_layout

    @pyqtSlot(int)
    def use_method(self, method):
        self.teaching_method = method
        self.teaching_method_changed.emit(method)

    # TODO
    # @pyqtSlot()
    # def set_item_info(self):
    #     self.cart_items.setText(f"Przedmioty: {self.cart.palette.items}")



