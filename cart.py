from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem

from board_items import RandomItem


class Cart(QTableWidgetItem):

    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("images/forklift.svg"))
        self.forward_icon = QIcon("images/forklift_front.png")
        self.backward_icon = QIcon("images/forklift_back.png")
        self.rightward_icon = QIcon("images/forklift_right.png")
        self.leftward_icon = QIcon("images/forklift_left.png")
        # self.has_item = False
        self.item = None

    def set_item(self, item: RandomItem):
        self.item = item

    def get_item(self):
        return self.item

    def has_item(self):
        return self.item is not None
