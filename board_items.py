import json
import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QTableWidgetItem


class RandomItem(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("images/package.png"))

        hardness = ['twarde', 'miekkie', 'kruche']
        weight = ['ciezkie', 'lekkie', 'srednie']
        size = ['male', 'srednie']
        shape = ['prostokatny', 'okragly', 'kolisty', 'brak', ]
        condensation = ['stale', 'ciekly']
        
        self.hardness = hardness[random.randint(0, 2)]
        self.weight = weight[random.randint(0, 2)]
        self.size = size[random.randint(0, 1)]
        self.shape = shape[random.randint(0, 3)]
        self.condensation = condensation[random.randint(0, 1)]

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
