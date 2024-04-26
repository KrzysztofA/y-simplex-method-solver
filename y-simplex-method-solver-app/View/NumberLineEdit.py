from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression


class NumberLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.validator = QRegularExpressionValidator()
        self.reg = QRegularExpression("0|[1-9][\\d]+/[\\d]+")
        self.validator.setRegularExpression(self.reg)
        self.setValidator(self.validator)
        self.setText("0")

    def get_value(self):
        return super().text()
