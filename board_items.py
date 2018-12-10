from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QTableWidgetItem


class RandomItem(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(22, 128, 65))
        self.setText("Przedmiot")


class PathCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(32, 88, 240))


class BlankCell(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setBackground(QColor(64, 64, 64))


class Obstacle(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        # self.setBackground(QColor(255, 0, 0))
        # self.setText("Przeszkoda")
        self.setIcon(QIcon("images/crate.png"))
