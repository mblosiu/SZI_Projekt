from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem


class Section(QTableWidgetItem):

    def __init__(self, icon_path):
        super().__init__()
        self.setIcon(QIcon(icon_path))
        # self.setBackground(QBrush(QImage(icon_path)))


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
