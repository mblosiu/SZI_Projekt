import random
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QTableWidgetItem


class Cart(QTableWidgetItem):

    def __init__(self, x, y):
        super().__init__()
        self.setText("Wózek")
        self.setBackground(QColor(128, 244, 128))
        self.x = x
        self.y = y
        self.palette = None


class Item(QTableWidgetItem):

    def __init__(self, x, y):
        super().__init__()
        self.setBackground(QColor(255, 0, 0))
        self.x = x
        self.y = y


class Goal(QTableWidgetItem):

    def __init__(self, x, y):
        super().__init__()
        self.setText("Cel")
        self.setBackground(QColor(0, 0, 255))
        self.x = x
        self.y = y

class BoardWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1366, 866)
        # self.setEnabled(False)
        self.method = None

        self.table = QTableWidget(25, 25)
        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 10)
        # self.clear_table()

        self.cart = Cart(random.randrange(0, self.table.columnCount()), random.randrange(0, self.table.rowCount()))
        self.table.setItem(self.cart.x, self.cart.y, self.cart)

        self.goal = Goal(random.randrange(0, self.table.columnCount()), random.randrange(0, self.table.rowCount()))
        self.table.setItem(self.goal.x, self.goal.y, self.goal)

        self.populate_table()

        self.lin = QHBoxLayout()
        self.lin.addWidget(self.table)

        self.setLayout(self.lin)

    # def clear_table(self):
            #
            # for j in range(self.table.rowCount()):
            #     self.table.setItem(i, j, QTableWidgetItem())

    def populate_table(self):
        count = random.randint(0, 50)
        for i in range(count):
            x = random.randrange(0, self.table.columnCount())
            y = random.randrange(0, self.table.rowCount())

            if self.table.item(x, y) is None:
                item = Item(x, y)
                self.table.setItem(x, y, item)

    @pyqtSlot()
    def use_method(self, str):
        if self.method is None:
            self.method = str
        else:
            print(self.method)

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
