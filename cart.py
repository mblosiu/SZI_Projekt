import enum

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem


class Cart(QTableWidgetItem):

    class Orientation(enum.Enum):
        NORTH = 1,
        EAST = 2,
        SOUTH = 3,
        WEST = 4

    MAX_ITEMS = 5

    def __init__(self, orientation: Orientation = Orientation.NORTH):
        super().__init__()

        self.icon_dict = {
            self.Orientation.NORTH: QIcon("images/forklift_front.png"),
            self.Orientation.EAST: QIcon("images/forklift_right.png"),
            self.Orientation.SOUTH: QIcon("images/forklift_back.png"),
            self.Orientation.WEST: QIcon("images/forklift_left.png")
        }

        self.setIcon(self.icon_dict[orientation])

        self.palette = []
        self.transports_items = False
        self.sections_to_go = []

    def __str__(self):
        s = ""

        for item in self.palette:
            s += str(item)

        return s

    def get_item(self, index):
        return self.palette[index]

    def has_item(self):
        return len(self.palette) > 0

    def add_item(self, item):
        self.palette.append(item)

    def full_capacity(self):
        return len(self.palette) == self.MAX_ITEMS
