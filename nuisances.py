from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem


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
