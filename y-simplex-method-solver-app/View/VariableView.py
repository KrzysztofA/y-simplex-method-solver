from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from .NumberLineEdit import NumberLineEdit


class VariableView(QWidget):
    def __init__(self, no: int):
        super().__init__()
        self.setLayout(QHBoxLayout())
        if no != 0:
            self.layout().addWidget(QLabel(f"+"))
        self.layout().addWidget(NumberLineEdit())
        self.layout().addWidget(QLabel(f"x{no}"))
