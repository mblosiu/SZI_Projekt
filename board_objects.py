import enum
import random
from typing import List

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem


class BoardObject(QTableWidgetItem):

    def __init__(self, icon_path: str = None):
        super().__init__()

        if icon_path:
            self.setIcon(QIcon(icon_path))

    def pos(self):
        return self.row(), self.column()


class RandomItem(BoardObject):

    def __init__(self):
        super().__init__("images/package.png")

        hardness = ['twarde', 'miekkie', 'kruche']
        weight = ['ciezkie', 'lekkie', 'srednie']
        size = ['male', 'srednie']
        shape = ['prostokatny', 'okragly', 'kolisty', 'brak', ]
        condensation = ['stale', 'ciekly']
        przeznaczenie = ['dzieci', 'dorosli', 'wszyscy', 'chorzy']

        self.hardness = hardness[random.randint(0, 2)]
        self.weight = weight[random.randint(0, 2)]
        self.size = size[random.randint(0, 1)]
        self.shape = shape[random.randint(0, 3)]
        self.condensation = condensation[random.randint(0, 1)]
        self.przeznaczenie = przeznaczenie[random.randint(0, 3)]

        self.attributes = {
            "twardosc": self.hardness,
            "waga": self.weight,
            "wielkosc": self.size,
            "ksztalt": self.shape,
            "skupienie": self.condensation,
            "przeznaczenie": self.przeznaczenie
        }

    def __str__(self):
        s = ""

        for attr in self.attributes.keys():
            s += f"{attr}: {self.attributes[attr]}\n"

        s += "\n"

        return s


class Direction(enum.Enum):
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4


class Cart(BoardObject):

    def __init__(self, direction: Direction = Direction.NORTH):

        self.icon_dict = {
            Direction.NORTH: QIcon("images/forklift_front.png"),
            Direction.EAST: QIcon("images/forklift_right.png"),
            Direction.SOUTH: QIcon("images/forklift_back.png"),
            Direction.WEST: QIcon("images/forklift_left.png")
        }


        super().__init__(self.icon_dict[direction])

        self.MAX_ITEMS = 7
        self.palette = []
        self.palette_sections = []
        self.transports_items = False
        self.direction = direction

    def __str__(self):
        s = ""

        for item in self.palette:
            s += str(item)

        return s

    def get_item(self, index) -> RandomItem:
        return self.palette[index]

    def has_item(self) -> bool:
        return len(self.palette) > 0

    def add(self, item: RandomItem):
        self.palette.append(item)

    def full(self) -> bool:
        return len(self.palette) == self.MAX_ITEMS

    def empty(self) -> bool:
        return len(self.palette) == 0

    def change_direction(self, direction):

        if direction == 'u':
            if self.direction in [Direction.EAST, Direction.WEST]:
                self.setIcon(self.icon_dict[Direction.NORTH])
                self.direction = Direction.NORTH
                return True
            elif self.direction == Direction.SOUTH:
                self.setIcon(self.icon_dict[Direction.WEST])
                self.direction = Direction.WEST
                return True
            else:
                return False

        if direction == 'l':
            if self.direction in [Direction.NORTH, Direction.SOUTH]:
                self.setIcon(self.icon_dict[Direction.WEST])
                self.direction = Direction.WEST
                return True
            elif self.direction == Direction.EAST:
                self.setIcon(self.icon_dict[Direction.NORTH])
                self.direction = Direction.NORTH
                return True
            else:
                return False

        if direction == 'r':
            if self.direction in [Direction.NORTH, Direction.SOUTH]:
                self.setIcon(self.icon_dict[Direction.EAST])
                self.direction = Direction.EAST
                return True
            elif self.direction == Direction.WEST:
                self.setIcon(self.icon_dict[Direction.NORTH])
                self.direction = Direction.NORTH
                return True
            else:
                return False

        if direction == 'd':
            if self.direction in [Direction.EAST, Direction.WEST]:
                self.setIcon(self.icon_dict[Direction.SOUTH])
                self.direction = Direction.SOUTH
                return True
            elif self.direction == Direction.NORTH:
                self.setIcon(self.icon_dict[Direction.EAST])
                self.direction = Direction.EAST
                return True
            else:
                return False

        return False


class Obstacle(BoardObject):

    def __init__(self):
        super().__init__("images/crate.png")


class TechSection(BoardObject):

    def __init__(self):
        super().__init__("images/tech.png")


class FoodSection(BoardObject):

    def __init__(self):
        super().__init__("images/food.png")


class ClothSection(BoardObject):

    def __init__(self):
        super().__init__("images/cloth.png")


class PaperSection(BoardObject):

    def __init__(self):
        super().__init__("images/paper.png")


class FloraSection(BoardObject):

    def __init__(self):
        super().__init__("images/flora.png")


class MedicineSection(BoardObject):

    def __init__(self):
        super().__init__("images/medicine.png")


class ToySection(BoardObject):

    def __init__(self):
        super().__init__("images/toys.png")


# Pola, przez które wózek może przejść

class PassableObject(BoardObject):

    def __init__(self, cost: int, icon_path: str = None):
        super().__init__(icon_path)
        self.cost = cost


class BlankCell(PassableObject):

    def __init__(self):
        super().__init__(1)


class GlassNuisance(PassableObject):

    def __init__(self):
        super().__init__(2, "images/shattered_glass.png")


class PlankNuisance(PassableObject):

    def __init__(self):
        super().__init__(3, "images/wood_plank.png")


class WaterNuisance(PassableObject):

    def __init__(self):
        super().__init__(4, "images/water_splash.png")
