from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class Nuisance(QTableWidgetItem):

    def __init__(self, cost: int, icon):
        super().__init__()
        self.cost = cost
        self.setBackground(icon)


class GlassNuisance(Nuisance):

    def __init__(self):
        super().__init__(2, Qt.darkCyan)


class PlankNuisance(Nuisance):

    def __init__(self):
        super().__init__(3, Qt.blue)
