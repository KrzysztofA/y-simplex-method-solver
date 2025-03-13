from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt


class SettingsMenu(QWidget):
    """
    Widget containing the menu buttons for the settings dialogue.
    """
    def __init__(self, to_change: QStackedWidget):
        super().__init__()
        self.to_change = to_change
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.buttons = []
        self.buttons.append(QPushButton('General'))
        self.buttons[-1].clicked.connect(lambda: self.select_button(0))
        self.buttons.append(QPushButton('Editor'))
        self.buttons[-1].clicked.connect(lambda: self.select_button(1))
        #TODO: Implement the following sections
        # self.buttons.append(QPushButton('Export'))
        # self.buttons[-1].clicked.connect(lambda: self.select_button(2))
        # self.buttons.append(QPushButton('Performance'))
        # self.buttons[-1].clicked.connect(lambda: self.select_button(3))
        self.vbox.setContentsMargins(0, 10, 0, 0)
        self.select_button(0)
        for button in self.buttons:
            self.vbox.addWidget(button)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

    def select_button(self, index: int):
        """
        Selects the settings with the given index. Includes changing the color of the button with the given index to active color.
        """
        self.buttons[index].setStyleSheet("background-color: rgba(60, 60, 60, 1); ")
        for button in enumerate(self.buttons):
            if button[0] == index:
                continue
            button[1].setStyleSheet("background-color: rgba(0, 0, 0, 0); ")
        self.to_change.setCurrentIndex(index)
