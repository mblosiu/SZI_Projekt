import heapq
import random

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, \
    QTableWidgetItem, QTableWidget

from sections import FloraSection, PaperSection, ClothSection, FoodSection, \
    TechSection


class RandomItem(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(22, 128, 65))
        self.setText("Przedmiot")


class Obstacle(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(255, 0, 0))
        self.setText("Przeszkoda")


class PathCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(32, 88, 240))


class BlankCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(64, 64, 64))


class GameBoard(QTableWidget):

    item_spawned = pyqtSignal(int, int)
    cart_moved = pyqtSignal(int, int, QTableWidgetItem)
    cart_picked_item = pyqtSignal()
    cart_picked_item_pos = pyqtSignal(int, int)
    cart_dropped_item = pyqtSignal()

    def __init__(self, rows, columns, board):
        super().__init__(rows, columns)

        for x in range(self.rowCount()):
            for y in range(self.columnCount()):
                self.setItem(x, y, BlankCell())

        self.board = board
        self.__add_obstacles()
        self.__add_sections()

        self.board_items = []

        self.cart_picked_item.connect(self.board.set_item_info)
        self.cart_dropped_item.connect(self.board.set_item_info)
        self.cart_picked_item_pos.connect(self.remove_item)
        self.cart_moved.connect(self.move_cart)

    def __add_obstacles(self):
        for i in range(random.randint(5, 25)):
            rand_x = random.randint(2, self.rowCount() - 3)
            rand_y = random.randint(0, self.columnCount() - 1)
            if isinstance(self.item(rand_x, rand_y), BlankCell):
                self.setItem(rand_x, rand_y, Obstacle())

    def __add_sections(self):

        self.sections = [
            TechSection(self.rowCount() - 1, 0),
            FoodSection(self.rowCount() - 1, 5),
            FloraSection(self.rowCount() - 1, 10),
            PaperSection(self.rowCount() - 1, 15),
            ClothSection(self.rowCount() - 1, 19),
        ]

        for section in self.sections:
            self.setItem(section.x, section.y, section)

    @pyqtSlot(int, int)
    def remove_item(self, x, y):
        self.setItem(x, y, BlankCell())
        # print(self.board_items)
        # print((x, y))
        self.board_items.remove((x, y))


    @pyqtSlot()
    def spawn_item(self):
        rand = random.randrange(self.columnCount())
        if isinstance(self.item(0, rand), BlankCell):
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


class Cart(QTableWidgetItem):

    def is_route_calculated(self):
        return self.route_calculated

    def coordinates(self):
        return self.x, self.y

    # def items(self):
    #     return self.palette.items

    def holds_item(self):
        return len(self.palette.items) > 0

    def calc_route(self, x, y):
        if self.is_route_calculated() is False:
            self.route_calculated = True
            self.cartastar(x + 1, y)

    class Palette:
        def __init__(self, capacity: int, items: list):
            self.capacity = capacity
            self.items = items

    def __init__(self, x: int, y: int, table: GameBoard):
        super().__init__()
        self.setText("Wózek")
        self.setIcon(QIcon("forklift.svg"))
        self.x = x
        self.y = y
        self.table = table
        self.palette = self.Palette(1, [])
        self.route_calculated = False
        self.path = []
        self.move_timer = QTimer()
        self.goal_coords = None
        self.item = None

        self.table.item_spawned.connect(self.calc_route)
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
                        self.table.cart_picked_item_pos.emit(
                            self.goal_coords[0] - 1, self.goal_coords[1])
                        self.table.cart_picked_item.emit()
                    else:
                        self.item = None
                        self.palette.items.pop(0)
                        self.table.cart_dropped_item.emit()

                    # Przenieś przedmiot do sekcji
                    if self.item == 1:
                        random_section_number = random.randrange(5)
                        self.cartastar(
                            self.table.sections[random_section_number].row(),
                            self.table.sections[random_section_number].column())
                    # Idź po przedmiot
                    else:
                        random_item = random.randrange(len(self.table.board_items))
                        random_item = self.table.board_items[random_item]
                        self.cartastar(random_item[0] + 1, random_item[1])

    # FIXME BIG
    def cartastar(self, goal_x, goal_y):
        cart_coordinates = (self.row(), self.column())
        goal_coordinates = (goal_x, goal_y)

        frontier = PQueue()
        frontier.put(cart_coordinates, 0)

        came_from = {cart_coordinates: None}
        cost_so_far = {cart_coordinates: 0}

        while not frontier.empty():
            current = frontier.get()

            if current == goal_coordinates:
                break

            for next_item in self.neighbors(current):

                new_cost = cost_so_far[current] + 1

                if next_item not in cost_so_far or new_cost < cost_so_far[next_item]:
                    cost_so_far[next_item] = new_cost
                    priority = new_cost + self.heuristic(goal_coordinates, next_item)
                    frontier.put(next_item, priority)
                    came_from[next_item] = current

        for i in came_from.values():
            if i is not None:
                if i != cart_coordinates and i != goal_coordinates:
                    if isinstance(self.table.item(i[0], i[1]), BlankCell):
                        self.path.append(i)
                        self.table.setItem(i[0], i[1], PathCell())

        # print(self.path)

        print(came_from.values())
        self.goal_coords = goal_coordinates
        print(self.goal_coords)
        # if self.item is not None:
        #     # self.goal_coords = (goal_coordinates[0] - 1, goal_coordinates[1])
        #     pos = self.path.pop(len(self.path) - 1)
        #     self.path.append((pos[0] - 1, pos[1]))
        #     # self.path[len(self.path) - 1]
        # else:
        #     pos = self.path.pop(len(self.path) - 1)
        #     self.path.append((pos[0] + 1, pos[1]))


    def neighbors(self, pos):
        (x, y) = pos
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        result = []

        for direction in directions:
            neighbor = (x + direction[0], y + direction[1])
            if 0 <= neighbor[0] <= self.table.rowCount() \
                    and 0 <= neighbor[1] <= self.table.columnCount():
                if not isinstance(self.table.item(neighbor[0], neighbor[1]), Obstacle):
                    result.append(neighbor)

        return result

    @staticmethod
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        # print(abs(x1 - x2) + abs(y1 - y2))
        return abs(x1 - x2) + abs(y1 - y2)


class PQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class BoardWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1366, 866)

        self.table = GameBoard(20, 20, self)

        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 60)

        self.cart = Cart(random.randrange(1, self.table.rowCount() - 1),
                         random.randrange(0, self.table.columnCount() - 1), self.table)
        self.table.setItem(self.cart.x, self.cart.y, self.cart)

        self.timer = QTimer()

        self.teaching_method = None

        lin = QVBoxLayout()
        lin.addWidget(QLabel("Program: Wózek widłowy"))

        self.cart_items = QLabel(f"Przedmioty: {self.cart.palette.items}")
        lin.addWidget(self.cart_items)

        lin.addWidget(self.table)

        info_layout = QHBoxLayout()
        info_layout.addLayout(lin)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(info_layout)

        self.setLayout(self.main_layout)

    item_spawned = pyqtSignal(int, int)

    def start_simulation(self):
        self.timer.timeout.connect(self.table.spawn_item)
        self.timer.start(1000)
        self.cart.move_timer.start(100)

    def use_method(self, method):
        if self.teaching_method is None:
            self.teaching_method = method
            self.start_simulation()

    @pyqtSlot()
    def set_item_info(self):
        self.cart_items.setText(f"Przedmioty: {self.cart.palette.items}")

