from PyQt6.QtWidgets import QScrollArea, QLabel, QVBoxLayout, QSizePolicy, QWidget
from PyQt6.QtCore import Qt
from .Function import Function
from .Constraint import Constraint


class InputBox(QScrollArea):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        label = QLabel("Function:")
        label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.layout.addWidget(label)

        self.widget = QWidget(self)
        self.setWidget(self.widget)
        self.function = Function()
        self.layout.addWidget(self.function)
        self.setMinimumSize(320, 250)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        self.constraints = []
        self.var_no = 2
        self.widget.setLayout(self.layout)
        self.set_constraints(2)

    def synchronize_variables(self, var_no: int):
        self.var_no = var_no
        for constraint in self.constraints:
            constraint.synchronize_variables(var_no)
        self.function.synchronize_variables(var_no)

    def set_constraints(self, const_no: int):
        if const_no < len(self.constraints):
            for i in self.constraints[const_no:]:
                self.layout.removeWidget(i)
                self.constraints.remove(i)
        else:
            old_len = len(self.constraints)
            for i in range(len(self.constraints), const_no):
                self.constraints.append(Constraint(self.var_no))
            for i in range(old_len, len(self.constraints)):
                self.layout.addWidget(self.constraints[i])
