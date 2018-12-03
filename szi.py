import sys

from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton

from boardwindow import BoardWindow


class SziWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.board_window = BoardWindow()

    def init_ui(self):
        self.setWindowTitle("AI - Wózek widłowy")
        self.setLayout(self.get_start_menu())
        self.show()

    def get_start_menu(self):
        methods_layout = QVBoxLayout()
        methods_layout.setContentsMargins(75, 75, 75, 75)

        teaching_methods = [
            "Drzewa decyzyjne",
            "Algorytmy genetyczne",
            "Sieci neuronowe"
        ]

        for method in teaching_methods:
            method_button = QPushButton(method)
            method_button.clicked.connect(self.use_teaching_method)
            methods_layout.addWidget(method_button)

        return methods_layout

    @pyqtSlot()
    def use_teaching_method(self):
        self.board_window.use_method(self.sender().text())
        self.board_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SziWindow()

    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = exception_hook
    app.exec()
