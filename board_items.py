import json
import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QTableWidgetItem


class RandomItem(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("images/package.png"))

        self.hardness = random.randint(1, 10)
        self.weight = random.randint(1, 20)
        self.size = random.randint(1, 20)
        self.shape = random.randint(1, 10)
        self.condensation = random.randint(1, 5)

        self.attributes = {
            "twardosc": self.hardness,
            "waga": self.weight,
            "wielkosc": self.size,
            "ksztalt": self.shape,
            "skupienie": self.condensation,
        }

    def get_attributes(self):
        return json.dumps(self.attributes)


class PathCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(Qt.blue)


class BlankCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(64, 64, 64))
        self.cost = 1


class Obstacle(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("images/crate.png"))
