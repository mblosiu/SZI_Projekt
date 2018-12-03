import heapq
import heapq
import random

from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidget, QWidget, \
    QTableWidgetItem, QVBoxLayout

from sections import ClothSection, PaperSection, FloraSection, FoodSection, \
    TechSection


class GameBoard(QTableWidget):

    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.cart_moved.connect(self.move_cart)

        tech = TechSection(self.rowCount() - 1, 0)
        food = FoodSection(self.rowCount() - 1, 5)
        flora = FloraSection(self.rowCount() - 1, 10)
        paper = PaperSection(self.rowCount() - 1, 15)
        cloth = ClothSection(self.rowCount() - 1, 19)

        self.sections = [
            tech,
            food,
            flora,
            paper,
            cloth
        ]

        for s in self.sections:
            self.setItem(s.xs, s.ys, s)

        # Optional obstacles
        for i in range(random.randint(0, 20)):
            rand_x = random.randint(1, self.rowCount() - 2)
            rand_y = random.randint(0, self.columnCount() - 1)
            if self.item(rand_x, rand_y) is None:
                self.setItem(rand_x, rand_y, Obstacle())

        self.board_items = []

    @pyqtSlot()
    def spawn_item(self):
        rand = random.randrange(self.columnCount())
        if self.item(0, rand) is None:
            y = random.randrange(self.columnCount())
            self.setItem(0, y, RandomItem())
            self.board_items.append((0, y))
            self.item_spawned.emit(0, y)

    item_spawned = pyqtSignal(int, int)
    cart_moved = pyqtSignal(int, int, QTableWidgetItem)

    @pyqtSlot(int, int, QTableWidgetItem)
    def move_cart(self, x, y, cart):
        self.takeItem(cart.row(), cart.column())
        self.setItem(x, y, cart)


class Cart(QTableWidgetItem):

    def __init__(self, x: int, y: int, table: GameBoard):
        super().__init__()
        self.setText("Wózek")
        self.setIcon(QIcon("forklift.svg"))
        self.x = x
        self.y = y
        self.table = table
        self.table.item_spawned.connect(self.calc_route)
        self.palette = self.Palette(1, [])
        self.route_calculated = False
        self.path = []
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_cart)
        self.item = None

    def move_cart(self):
        if len(self.path) > 0:
            if self.path[0] is not None:
                self.table.cart_moved.emit(self.path[0][0], self.path[0][1], self)
            self.path.pop(0)

            if len(self.path) == 0:
                # self.held_item_changed.emit()
                if self.item is None:
                    self.item = 1
                else:
                    self.item = None

                if self.item == 1:
                    random_section_number = random.randrange(5)
                    self.cartastar(self.table.sections[random_section_number].row(),
                                   self.table.sections[random_section_number].column())
                else:
                    random_item = random.randrange(len(self.table.board_items))
                    random_item = self.table.board_items[random_item]
                    self.cartastar(random_item[0], random_item[1])

    # held_item_changed = pyqtSignal()

    # @pyqtSlot()
    # def move_item(self):
    #     if self.item is None:
    #         self.item = 1
    #     else:
    #         self.item = None

    # @pyqtSlot()
    # def drop_item(self):
    #     self.item = None

    def is_route_calculated(self):
        return self.route_calculated

    def coordinates(self):
        return self.x, self.y

    def items(self):
        return self.palette.items

    def holds_item(self):
        return len(self.palette.items) > 0

    def calc_route(self, x, y):
        if self.is_route_calculated() is False:
            self.route_calculated = True
            self.cartastar(x, y)

    class Palette:
        def __init__(self, capacity: int, items: list):
            self.capacity = capacity
            self.items = items

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

            for next_item in neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next_item not in cost_so_far or new_cost < cost_so_far[next_item]:
                    cost_so_far[next_item] = new_cost
                    priority = new_cost + heuristic(goal_coordinates, next_item)
                    frontier.put(next_item, priority)
                    came_from[next_item] = current

        for i in came_from.values():
            if i is not None:
                if i != cart_coordinates and i != goal_coordinates:
                    self.path.append(i)
                    self.table.setItem(i[0], i[1], GoodCell())

        print(self.path)

    def neighbors(self):
        (x, y) = self.row(), self.column()
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        result = []

        for direction in directions:
            neighbor = (x + direction[0], y + direction[1])
            # if table.item(neighbor[0], neighbor[1]) is None:
            #     result.append(neighbor)
            if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 20:
                result.append(neighbor)

        return result


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


class GoodCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(32, 88, 240))


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


class BoardWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1366, 866)

        self.table = GameBoard(20, 20)

        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 60)

        # for x in range(self.table.rowCount()):
        #     for y in range(self.table.columnCount()):
        #         self.table.setItem(x, y, QTableWidgetItem())

        self.cart = Cart(random.randrange(1, self.table.rowCount() - 1),
                         random.randrange(0, self.table.columnCount() - 1), self.table)
        self.table.setItem(self.cart.x, self.cart.y, self.cart)

        self.timer = QTimer()

        self.teaching_method = None

        lin = QVBoxLayout()
        lin.addWidget(QLabel("Program: Wózek widłowy"))

        self.cart_items = QLabel(f"Przedmioty: {self.cart.items()}")
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
        self.cart.move_timer.start(500)

    def use_method(self, method):
        if self.teaching_method is None:
            self.teaching_method = method
            self.start_simulation()






# def neighbors(table: QTableWidget, item: QTableWidgetItem, goal: QTableWidgetItem):
#     directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
#     result = []
#
#     for direction in directions:
#         neighbor = (item.row() + direction[0], item.column() + direction[1])
#         if table.item(neighbor[0], neighbor[1]) is None:
#             result.append(neighbor)
#         # if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 20:
#         #     result.append(neighbor)
#
#     return result


def neighbors(a):
    (x, y) = a
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    result = []

    for direction in directions:
        neighbor = (x + direction[0], y + direction[1])
        # if table.item(neighbor[0], neighbor[1]) is None:
        #     result.append(neighbor)
        if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 20:
            result.append(neighbor)

    return result


class PQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]



    # def astar(self, item: QTableWidgetItem, goal: QTableWidgetItem):
    #     item_coordinates = (item.row(), item.column())
    #     goal_coordinates = (goal.row(), goal.column())
    #
    #     frontier = PQueue()
    #     frontier.put(item_coordinates, 0)
    #
    #     came_from = {item_coordinates: None}
    #     cost_so_far = {item_coordinates: 0}
    #
    #     while not frontier.empty():
    #         current = frontier.get()
    #
    #         if current == goal_coordinates:
    #             break
    #
    #         for next_item in neighbors(current):
    #             new_cost = cost_so_far[current] + 1
    #             if next_item not in cost_so_far or new_cost < cost_so_far[next_item]:
    #                 cost_so_far[next_item] = new_cost
    #                 priority = new_cost + heuristic(goal_coordinates, next_item)
    #                 frontier.put(next_item, priority)
    #                 came_from[next_item] = current
    #
    #     for i in came_from.values():
    #         if i is not None:
    #             if i != item_coordinates and self.table.item(i[0], i[1]) is None:
    #                 self.table.setItem(i[0], i[1], GoodCell())
    #
    #     print(cost_so_far)