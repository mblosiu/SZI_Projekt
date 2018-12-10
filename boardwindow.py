from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget

from gameboard import GameBoard


class BoardWindow(QWidget):

    teaching_method_changed = pyqtSignal(int)

    def __init__(self, method):
        super().__init__()
        self.resize(1366, 866)
        self.cart_items = QLabel()
        self.setLayout(self.init_ui(method))
        self.show()
        self.teaching_method = None

    def init_ui(self, method):
        main_layout = QVBoxLayout()

        font = QFont("Sans", 12)

        name = QLabel(f"Agent: Wózek widłowy, Metoda: {method}")
        name.setFont(font)
        name.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(name)

        self.cart_items.setText(f"Przedmiot wózka: Brak")
        self.cart_items.setFont(font)
        self.cart_items.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.cart_items)

        table = GameBoard(20, 20, self)

        for i in range(table.columnCount()):
            table.setColumnWidth(i, 25)

        main_layout.addWidget(table)

        self.teaching_method_changed.connect(table.start_simulation)

        return main_layout

    @pyqtSlot(int)
    def use_method(self, method):
        self.teaching_method = method
        self.teaching_method_changed.emit(method)

    @pyqtSlot(str)
    def set_item_info(self, info):
        self.cart_items.setText(f"Przedmiot wózka: {info}")



