import enum
import sys

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
    QLabel

from boardwindow import BoardWindow


class TeachingMethod(enum.Enum):
    DECISION_TREE = 1,
    NEURAL_NETWORK = 2


class SziWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI - Wózek widłowy")
        self.setLayout(self.init_ui())
        self.show()

    class TeachingMethodButton(QPushButton):

        def __init__(self, method_id: TeachingMethod, text: str):
            super().__init__()
            self.method_id = method_id
            self.setText(text)

    def init_ui(self):
        menu_layout = QVBoxLayout()

        name = QLabel("Agent: Wózek widłowy")
        name.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(name)

        icon = QPixmap("images/forklift.svg")

        icon_label = QLabel()
        icon_label.setPixmap(icon)
        icon_label.setAlignment(Qt.AlignCenter)

        menu_layout.addWidget(icon_label)

        teaching_methods = {
            TeachingMethod.DECISION_TREE: "Drzewa decyzyjne",
            TeachingMethod.NEURAL_NETWORK: "Sieci neuronowe"
        }

        for method in teaching_methods:
            method_button = self.TeachingMethodButton(method,
                                                      teaching_methods[method])
            method_button.clicked.connect(lambda state,
                                                 m=method,
                                                 s=teaching_methods[method]:
                                          self.use_teaching_method(m, s))
            menu_layout.addWidget(method_button)

        return menu_layout

    @pyqtSlot(int, str)
    def use_teaching_method(self, method: TeachingMethod, method_name: str):
        BoardWindow(method_name)


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
