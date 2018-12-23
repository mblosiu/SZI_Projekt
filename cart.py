import enum

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem


class Cart(QTableWidgetItem):

    class Orientation(enum.Enum):
        NORTH = 1,
        EAST = 2,
        SOUTH = 3,
        WEST = 4

    def __init__(self, orientation: Orientation=Orientation.NORTH):
        super().__init__()

        self.icon_dict = {
            self.Orientation.NORTH: QIcon("images/forklift_front.png"),
            self.Orientation.EAST: QIcon("images/forklift_right.png"),
            self.Orientation.SOUTH: QIcon("images/forklift_back.png"),
            self.Orientation.WEST: QIcon("images/forklift_left.png")
        }

        self.setIcon(self.icon_dict[orientation])
        self.item = None

    def set_item(self, item):
        self.item = item

    def get_item(self):
        return self.item

    def has_item(self):
        return self.item is not None
