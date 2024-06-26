from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from .NumberLineEdit import NumberLineEdit


class VariableInputView(QWidget):
    def __init__(self, no: int, parent=None):
        super().__init__(parent)
        self.variable_edit = NumberLineEdit(self)
        self.setLayout(QHBoxLayout())
        if no != 0:
            self.layout().addWidget(QLabel(f"+"))
        self.layout().addWidget(self.variable_edit)
        self.layout().addWidget(QLabel(f"x{no}"))

    def get_value(self):
        return self.variable_edit.get_value()

    def set_value(self, value):
        self.variable_edit.set_value(value)
        