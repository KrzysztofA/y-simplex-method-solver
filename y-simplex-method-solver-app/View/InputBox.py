from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from .Function import Function
from .Constraint import Constraint


class InputBox(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        label = QLabel("Function:")
        self.layout.addWidget(label)
        self.function = Function()
        self.layout.addWidget(self.function)
        self.constraints = [Constraint(), Constraint()]
        for constraint in self.constraints:
            self.layout.addWidget(constraint)
            self.layout.addWidget(constraint)
        self.setLayout(self.layout)

    def synchronize_variables(self, var_no: int):
        for constraint in self.constraints:
            constraint.synchronize_variables(var_no)
        self.function.synchronize_variables(var_no)

