from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt


class SettingsMenu(QWidget):
    def __init__(self, to_change: QStackedWidget):
        super().__init__()
        self.to_change = to_change
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.buttons = []
        self.buttons.append(QPushButton('General'))
        self.buttons[-1].clicked.connect(self.select_general)
        self.vbox.setContentsMargins(0, 10, 0, 0)
        self.select_general()
        for button in self.buttons:
            self.vbox.addWidget(button)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

    def select_general(self):
        self.buttons[0].setStyleSheet("background-color: rgba(60, 60, 60, 1); ")
        for button in self.buttons[1:]:
            button.setStyleSheet("background-color: rgba(0, 0, 0, 0); ")
        self.to_change.setCurrentIndex(0)
