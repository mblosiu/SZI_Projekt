from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem


class Section(QTableWidgetItem):

    def __init__(self, x, y, color, text):
        super().__init__()
        self.setBackground(color)
        self.setText(text)
        self.x = x
        self.y = y


class TechSection(Section):

    def __init__(self, x, y):
        super().__init__(x, y, QColor(240, 0, 240), "Sprzęt RTV")


class FoodSection(Section):

    def __init__(self, x, y):
        super().__init__(x, y, QColor(240, 240, 0), "Żywność")


class ClothSection(Section):

    def __init__(self, x, y):
        super().__init__(x, y, QColor(0, 240, 240), "Odzież")


class PaperSection(Section):

    def __init__(self, x, y):
        super().__init__(x, y, QColor(127, 120, 64), "Art. papierowe")


class FloraSection(Section):

    def __init__(self, x, y):
        super().__init__(x, y, QColor(0, 230, 15), "Ogrodnictwo")
