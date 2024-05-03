from PyQt6.QtWidgets import QScrollArea, QLabel, QVBoxLayout, QSizePolicy, QWidget
from PyQt6.QtCore import Qt
from .ObjectiveFunction import ObjectiveFunction
from .Constraint import Constraint
from Model import ProblemType
from typing import Dict


class InputBox(QScrollArea):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        label = QLabel("Function:")
        label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.layout.addWidget(label)

        self.widget = QWidget(self)
        self.setWidget(self.widget)
        self.function = ObjectiveFunction()
        self.layout.addWidget(self.function)
        self.setMinimumSize(320, 250)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        self.constraints = []
        self.problem = ProblemType.Maximization
        self.var_no = 2
        self.widget.setLayout(self.layout)
        self.set_constraints(2)

    def set_problem(self, problem: ProblemType):
        self.problem = problem
        for constraint in self.constraints:
            constraint.set_problem(problem)
        self.function.set_problem(problem)

    def set_problem_int(self, problem_int: int):
        if problem_int == 0:
            self.set_problem(ProblemType.Maximization)
        elif problem_int == 1:
            self.set_problem(ProblemType.Minimization)

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
                self.constraints.append(Constraint(self.parentWidget(), self.var_no, self.problem))
            for i in range(old_len, len(self.constraints)):
                self.layout.addWidget(self.constraints[i])

    def get_all_variables(self):
        strings = [self.function.get_variables_string()]
        for constraint in self.constraints:
            strings.append(constraint.get_variables_string())
        return strings

    def get_function(self):
        return self.function.get_variables_string()

    def get_constraints(self):
        return [a.get_variables_string() for a in self.constraints]

    def get_all_list(self):
        return_list = [self.function.get_variables_float_list()]
        for constraint in self.constraints:
            return_list.append(constraint.get_variables_float_list())
        return return_list

    def set_function(self, function_string: str):
        self.function.set_variables_from_string(function_string)

    def set_constraints_values(self, constraints: Dict[int, str]):
        for i in range(0, len(self.constraints)):
            self.constraints[i].set_values_from_string(constraints[i])
