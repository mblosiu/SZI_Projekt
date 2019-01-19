from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, \
    QFormLayout

from gameboard import GameBoard


class BoardWindow(QWidget):

    teaching_method_changed = pyqtSignal(int)

    def __init__(self, method):
        super().__init__()
        self.cart_items = QLabel()
        self.ga_info = QLabel()
        self.setLayout(self.init_ui(method))
        self.showMaximized()
        self.teaching_method = None

    def init_ui(self, method):
        main_layout = QHBoxLayout()

        font = QFont("Sans", 12)

        # name = QLabel(f"Agent: Wózek widłowy, Metoda: {method}")
        # name.setFont(font)
        # name.setAlignment(Qt.AlignCenter)
        # main_layout.addWidget(name)

        self.cart_items.setText(f"\nAgent: Wózek widłowy\nPrzedmioty:")
        self.cart_items.setFont(font)
        self.cart_items.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.cart_items)

        table = GameBoard(20, 20, self, method)

        for i in range(table.columnCount()):
            table.setColumnWidth(i, 55)

        for i in range(table.rowCount()):
            table.setRowHeight(i, 45)

        table.setIconSize(QSize(45, 45))

        main_layout.addWidget(table)

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

        self.teaching_method_changed.connect(table.start_simulation)

        return main_layout

    @pyqtSlot(int)
    def use_method(self, method):
        self.teaching_method = method
        self.teaching_method_changed.emit(method)

    @pyqtSlot(str)
    def update_items_info(self, info):
        self.cart_items.setText(f"\nAgent: Wózek widłowy\nPrzedmioty:\n\n{info}")

    @pyqtSlot(str)
    def update_ga_info(self, info):
        self.ga_info.setText(info)


