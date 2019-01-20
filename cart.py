import enum

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem


class Direction(enum.Enum):
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4


class Cart(QTableWidgetItem):

    def __init__(self, orientation: Direction = Direction.NORTH):
        super().__init__()

        self.icon_dict = {
            Direction.NORTH: QIcon("images/forklift_front.png"),
            Direction.EAST: QIcon("images/forklift_right.png"),
            Direction.SOUTH: QIcon("images/forklift_back.png"),
            Direction.WEST: QIcon("images/forklift_left.png")
        }

        self.setIcon(self.icon_dict[orientation])

        self.MAX_ITEMS = 5
        self.palette = []
        self.transports_items = False
        self.sections_to_go = []
        self.direction = orientation

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

    def change_direction(self, direction):

        if direction == 'u':
            if self.direction in [Direction.EAST, Direction.WEST]:
                self.setIcon(self.icon_dict[Direction.NORTH])
                self.direction = Direction.NORTH
            elif self.direction == Direction.SOUTH:
                self.setIcon(self.icon_dict[Direction.WEST])
                self.direction = Direction.WEST
            return True

        if direction == 'l':
            if self.direction in [Direction.NORTH, Direction.SOUTH]:
                self.setIcon(self.icon_dict[Direction.WEST])
                self.direction = Direction.WEST
            elif self.direction == Direction.EAST:
                self.setIcon(self.icon_dict[Direction.NORTH])
                self.direction = Direction.NORTH
            return True

        if direction == 'r':
            if self.direction in [Direction.NORTH, Direction.SOUTH]:
                self.setIcon(self.icon_dict[Direction.EAST])
                self.direction = Direction.EAST
            elif self.direction == Direction.WEST:
                self.setIcon(self.icon_dict[Direction.NORTH])
                self.direction = Direction.NORTH
            return True

        if direction == 'd':
            if self.direction in [Direction.EAST, Direction.WEST]:
                self.setIcon(self.icon_dict[Direction.SOUTH])
                self.direction = Direction.SOUTH
            elif self.direction == Direction.NORTH:
                self.setIcon(self.icon_dict[Direction.EAST])
                self.direction = Direction.EAST
            return True

        return False
