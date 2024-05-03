from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression


class NumberLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.validator = QRegularExpressionValidator()
        self.reg = QRegularExpression("0|[1-9]([\\d]+/[\\d]+|/[\\d]+)")
        self.validator.setRegularExpression(self.reg)
        self.setValidator(self.validator)
        self.setText("0")

    def get_value(self):
        return super().text()

    def set_value(self, value):
        super().setText(value)
