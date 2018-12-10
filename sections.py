from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem


class Section(QTableWidgetItem):

    def __init__(self, icon):
        super().__init__()
        #self.setIcon(icon)
        self.setBackground(QColor(icon))


class TechSection(Section):

    def __init__(self):
        super().__init__(QColor(240, 0, 240))


class FoodSection(Section):

    def __init__(self):
        super().__init__(QColor(240, 240, 0))


class ClothSection(Section):

    def __init__(self):
        super().__init__(QColor(0, 240, 240))


class PaperSection(Section):

    def __init__(self):
        super().__init__(QColor(127, 120, 64))


class FloraSection(Section):

    def __init__(self):
        super().__init__(QColor(0, 230, 15))
