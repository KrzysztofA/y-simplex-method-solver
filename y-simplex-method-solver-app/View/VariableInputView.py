from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from .NumberLineEdit import NumberLineEdit


class VariableInputView(QWidget):
    def __init__(self, no: int):
        super().__init__()
        self.variable_edit = NumberLineEdit()
        self.setLayout(QHBoxLayout())
        if no != 0:
            self.layout().addWidget(QLabel(f"+"))
        self.layout().addWidget(self.variable_edit)
        self.layout().addWidget(QLabel(f"x{no}"))

    def get_value(self):
        return self.variable_edit.get_value()
