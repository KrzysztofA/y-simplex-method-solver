from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from .VariableView import VariableView


class Function(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        z_label = QLabel("Z = ")
        self.layout.addWidget(z_label)
        self.setLayout(self.layout)
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