from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, \
    QFormLayout

from gameboard import GameBoard


class BoardWindow(QWidget):

    def __init__(self, method):
        super().__init__()
        self.cart_items = QLabel()
        self.ga_info = QLabel()
        self.table = GameBoard(20, 20, self, method)
        self.setLayout(self.init_ui())
        self.showMaximized()

    def init_ui(self):
        main_layout = QHBoxLayout()

        font = QFont("Sans", 12)

        self.cart_items.setText(f"\nAgent: Wózek widłowy\nPrzedmioty:")
        self.cart_items.setFont(font)
        self.cart_items.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.cart_items)

        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 55)

        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i, 45)

        self.table.setIconSize(QSize(45, 45))

        main_layout.addWidget(self.table)

        ga_pic = QLabel()
        pic = QPixmap("images/dna.png")
        pic.setDevicePixelRatio(8)
        ga_pic.setPixmap(pic)
        self.ga_info.setFont(font)
        ga_title = QLabel("Algorytm genetyczny:")
        ga_title.setFont(font)

        ga_info = QFormLayout()
        ga_info.addRow(ga_pic, ga_title)
        ga_info.addRow(QLabel(""), self.ga_info)

        main_layout.addLayout(ga_info)

        return main_layout

    @pyqtSlot(str, name="Update cart items info")
    def update_items_info(self, info):
        self.cart_items.setText(f"\nAgent: Wózek widłowy\nPrzedmioty:\n\n{info}")

    @pyqtSlot(str, name="Update genetic algorithm info")
    def update_ga_info(self, info):
        self.ga_info.setText(info)


