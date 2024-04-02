from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression


class NumberLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.validator = QRegularExpressionValidator()
        self.reg = QRegularExpression("[\\d|/]+")
        self.validator.setRegularExpression(self.reg)
        self.setValidator(self.validator)
