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

    def __str__(self):
        s = ""

        for attr in self.attributes.keys():
            s += f"{attr}: {self.attributes[attr]}\n"

        s += "\n"

        return s


class PathCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(Qt.blue)


class BlankCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.cost = 1


class Obstacle(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("images/crate.png"))

#####
class CategorizedItem:

    def __init__(self, json_data):
        self.attributes = {}

        for k in json_data.keys():
            self.attributes[k] = json_data[k]

    def __str__(self):
        s = ""

        for attr in self.attributes.keys():
            s += f"{attr}: {self.attributes[attr]}\n"

        s += "\n"

        return s


class Section(QTableWidgetItem):

    def __init__(self, icon_path):
        super().__init__()
        self.setIcon(QIcon(icon_path))


class TechSection(Section):

    def __init__(self):
        super().__init__("images/tech.png")


class FoodSection(Section):

    def __init__(self):
        super().__init__("images/food.png")


class ClothSection(Section):

    def __init__(self):
        super().__init__("images/cloth.png")


class PaperSection(Section):

    def __init__(self):
        super().__init__("images/paper.png")


class FloraSection(Section):

    def __init__(self):
        super().__init__("images/flora.png")


class MedicineSection(Section):

    def __init__(self):
        super().__init__("images/medicine.png")


class ToySection(Section):

    def __init__(self):
        super().__init__("images/toys.png")


class Nuisance(QTableWidgetItem):

    def __init__(self, cost: int, icon):
        super().__init__()
        self.cost = cost
        self.setIcon(QIcon(icon))


class GlassNuisance(Nuisance):

    def __init__(self):
        super().__init__(2, "images/shattered_glass.png")


class PlankNuisance(Nuisance):

    def __init__(self):
        super().__init__(3, "images/wood_plank.png")


class WaterNuisance(Nuisance):

    def __init__(self):
        super().__init__(4, "images/water_splash.png")
