import collections
import heapq
import random
import threading
from queue import PriorityQueue, Queue

from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal, QThread
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidget, QWidget, \
    QTableWidgetItem, QVBoxLayout

from sections import ClothSection, PaperSection, FloraSection, FoodSection, \
    TechSection, Section


class Cart(QTableWidgetItem):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.setText("Wózek")
        self.setIcon(QIcon("forklift.svg"))
        self.x = x
        self.y = y
        self.palette = self.Palette(1, [])

    def coordinates(self):
        return self.x, self.y

    def items(self):
        return self.palette.items

    def holds_item(self):
        return len(self.palette.items) > 0

    class Palette:
        def __init__(self, capacity: int, items: list):
            self.capacity = capacity
            self.items = items


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

        self.table = QTableWidget(20, 20)

        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 60)

        # for x in range(self.table.rowCount()):
        #     for y in range(self.table.columnCount()):
        #         self.table.setItem(x, y, QTableWidgetItem())

        self.cart = Cart(random.randrange(1, self.table.rowCount() - 1),
                         random.randrange(0, self.table.columnCount() - 1))
        self.table.setItem(self.cart.x, self.cart.y, self.cart)

        tech = TechSection(self.table.rowCount() - 1, 0)
        food = FoodSection(self.table.rowCount() - 1, 5)
        flora = FloraSection(self.table.rowCount() - 1, 10)
        paper = PaperSection(self.table.rowCount() - 1, 15)
        cloth = ClothSection(self.table.rowCount() - 1, 19)

        self.sections = [
            tech,
            food,
            flora,
            paper,
            cloth
        ]

        for s in self.sections:
            self.table.setItem(s.xs, s.ys, s)

        # Optional obstacles
        for i in range(random.randint(0, 10)):
            rand_x = random.randint(1, self.table.rowCount() - 2)
            rand_y = random.randint(0, self.table.columnCount() - 1)
            if self.table.item(rand_x, rand_y) is None:
                self.table.setItem(rand_x, rand_y, Obstacle())

        self.spawn_timer = QTimer()

        self.timer = QTimer()

        self.teaching_method = None

        self.main_layout = QHBoxLayout()

        info_layout = QHBoxLayout()

        lin = QVBoxLayout()
        lin.addWidget(QLabel("Program: Wózek widłowy"))

        self.cart_items = QLabel(f"Przedmioty: {self.cart.items()}")
        lin.addWidget(self.cart_items)

        lin.addWidget(self.table)

        info_layout.addLayout(lin)

        self.main_layout.addLayout(info_layout)
        self.setLayout(self.main_layout)

    def spawn_item(self):
        if random.random() < 0.3:
            rand = random.randrange(self.table.columnCount())
            if self.table.item(0, rand) is None:
                y = random.randrange(self.table.columnCount())
                self.table.setItem(0, y, RandomItem())

    def start_simulation(self):
        self.timer.timeout.connect(self.spawn_item)
        self.timer.start(1000)
        # self.cart_mover_timer.timeout.connect(self.move_cart)
        # self.cart_mover_timer.start(3000)

    # def move_cart(self):
    #     if self.next_cart_position is not None:
    #         self.table.setItem(self.next_cart_position[0],
    #                            self.next_cart_position[1],
    #                            self.cart)


    def use_method(self, method):
        if self.teaching_method is None:
            self.teaching_method = method
            self.start_simulation()
            # print()
            # wot = (self.sections[3].row(), self.sections[3].column())
            # print(self.bfs(self.table, self.cart.coordinates(), wot))
            print(self.astar(self.table, self.cart, self.sections[3]))
            # print(self.astar(self.table, self.cart, self.sections[3]))

    def astar(self, table: QTableWidget, item: QTableWidgetItem, goal: QTableWidgetItem):
        item_coordinates = (item.row(), item.column())
        goal_coordinates = (goal.row(), goal.column())

        frontier = PQueue()
        frontier.put(item_coordinates, 0)

        came_from = {item_coordinates: None}
        cost_so_far = {item_coordinates: 0}

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
                if i != item_coordinates:
                    print(i)
                    self.table.setItem(i[0], i[1], GoodCell())

        print(cost_so_far)



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
