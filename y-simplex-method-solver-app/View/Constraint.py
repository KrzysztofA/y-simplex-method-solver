from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from View.NumberLineEdit import NumberLineEdit
from .VariableView import VariableView


class Constraint(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.equals = NumberLineEdit()
        self.eq_label = QLabel(" = ")
        self.layout.addWidget(self.equals)
        self.layout.addWidget(self.eq_label)
        self.vars = []
        self.synchronize_variables(2)

    def synchronize_variables(self, var_no: int):
        if var_no < len(self.vars):
            for i in self.vars[var_no:]:
                self.layout.removeWidget(i)
                self.vars.remove(i)
        else:
            old_len = len(self.vars)
            for i in range(len(self.vars), var_no):
                self.vars.append(VariableView(i))
            for i in range(old_len, len(self.vars)):
                self.layout.addWidget(self.vars[i])

