import random
import sys
from queue import Queue

from PyQt5.QtCore import pyqtSlot, QSize, QTimer
from PyQt5.QtGui import QColor, QIcon, QImage, QBrush
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, \
    QTableWidgetItem, QLabel, QListWidget


class Palette:
    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items

class Cart(QTableWidgetItem):

    def __init__(self, x, y):
        super().__init__()
        self.setText("Wózek")
        icon = QIcon("forklift.svg")
        self.setIcon(icon)
        self.x = x
        self.y = y
        self.palette = None


# class Item(QTableWidgetItem):
#
#     def __init__(self, x, y):
#         super().__init__()
#         self.setBackground(QColor(255, 0, 0))
#         self.x = x
#         self.y = y


# class Goal(QTableWidgetItem):
#
#     def __init__(self, x, y):
#         super().__init__()
#         self.setBackground(QColor(0, 0, 255))
#         self.x = x
#         self.y = y


class Section(QTableWidgetItem):

    def __init__(self, xs, ys, color, text):
        super().__init__()
        self.xs = xs
        self.ys = ys
        self.setBackground(color)
        self.setText(text)


class TechSection(Section):

    def __init__(self, xs, ys):
        super().__init__(xs, ys, QColor(240, 0, 240), "Sprzęt RTV")
#


class FoodSection(Section):

    def __init__(self, xs, ys):
        super().__init__(xs, ys, QColor(240, 240, 0), "Żywność")


class ClothSection(Section):

    def __init__(self, xs, ys):
        super().__init__(xs, ys, QColor(0, 240, 240), "Odzież")


class PaperSection(Section):

    def __init__(self, xs, ys):
        super().__init__(xs, ys, QColor(127, 120, 64), "Art. papierowe")


class FloraSection(Section):

    def __init__(self, xs, ys):
        super().__init__(xs, ys, QColor(0, 230, 15), "Ogrodnictwo")


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


# def get_neighbors(table: QTableWidget, item: QTableWidgetItem):
#     north = table.item(item.row() - 1, item.column())
#     east = table.item(item.row(), item.column() + 1)
#     south = table.item(item.row() + 1, item.column())
#     west = table.item(item.row(), item.column() - 1)
#
#
#     # neighbors = [north, east, south, west]
#     neighbors = [
#         (north.row(), north.column()),
#         (east.row(), east.column()),
#         (west.row(), west.column()),
#         (south.row(), south.column()),
#     ]
#     return neighbors
#
# def get_coord_neighbors(coords):
#     # x = (4, 3)
#
#     north = (coords.index(0) - 1, coords.index(1))
#     east = (coords.index(0), coords.index(1) + 1)
#     south = (coords.index(0) + 1, coords.index(1))
#     west = (coords.index(0), coords.index(1) - 1)
#
#     neighbors = [
#         north,
#         east,
#         south,
#         west
#     ]
#     return neighbors

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

        self.cart = Cart(random.randrange(1, self.table.columnCount()), random.randrange(0, self.table.rowCount() - 1))
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

        # for x in range(self.table.rowCount()):
        #     if self.table.item(x, 0) is None:
        #         print("Tak")

        self.timer = QTimer()
        # self.timer.timeout.connect(self.hello)
        # self.timer.start(1000)

        self.teaching_method = None

        # self.info_layout = ()
        # self.info_layout.addWidget()
        # self.info_layout.addWidget(QLabel("Przedmioty:"))

        self.lin = QHBoxLayout()
        self.lin.addWidget(QLabel("Wózek widłowy"))
        self.lin.addWidget(self.table)
        self.setLayout(self.lin)

    # def hello(self):
    #     self.table.setItem(random.randrange(10), random.randrange(10), Cart(5, 5))
    #     print("Hi")

    # def clear_table(self):
            #
            # for j in range(self.table.rowCount()):
            #     self.table.setItem(i, j, QTableWidgetItem())

    # def populate_table(self):
    #     count = random.randint(0, 50)
    #     for i in range(count):
    #         x = random.randrange(0, self.table.columnCount())
    #         y = random.randrange(0, self.table.rowCount())
    #
    #         if self.table.item(x, y) is None:
    #             item = Item(x, y)
    #             self.table.setItem(x, y, item)

    def spawn_item(self):
        if random.random() < 0.3:
            rand = random.randrange(self.table.columnCount())
            if self.table.item(0, rand) is None:
                self.table.setItem(0, random.randrange(self.table.columnCount()), RandomItem())

    def start_simulation(self):
        self.timer.timeout.connect(self.spawn_item)
        self.timer.start(1000)

    def use_method(self, met):
        if self.teaching_method is None:
            self.teaching_method = met
            self.start_simulation()


class SziWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.board_window = BoardWindow()

    def init_ui(self):
        self.setWindowTitle("AI - Wózek widłowy")
        self.setLayout(self.get_start_menu())
        self.show()

    def get_start_menu(self):
        methods_layout = QVBoxLayout()
        methods_layout.setContentsMargins(75, 75, 75, 75)

        teaching_methods = [
            "Drzewa decyzyjne",
            "Algorytmy genetyczne",
            "Sieci neuronowe"
        ]

        for method in teaching_methods:
            method_button = QPushButton(method)
            method_button.clicked.connect(self.use_teaching_method)
            methods_layout.addWidget(method_button)

        return methods_layout

    @pyqtSlot()
    def use_teaching_method(self):
        self.board_window.use_method(self.sender().text())
        self.board_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SziWindow()
    app.exec()
