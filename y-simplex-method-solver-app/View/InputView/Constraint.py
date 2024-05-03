from PyQt6.QtWidgets import QWidget
from Model import ProblemType
from .Function import Function, Sign


class Constraint(Function):
    def __init__(self, parent: QWidget | None = None, variable_number: int = 2, problem_type: ProblemType = ProblemType.Maximization):
        super().__init__(variable_number, None, parent, Sign.Less, Sign.Greater, problem_type)

    def set_values_from_string(self, constraint_string: str):
        constraint = [a.strip() for a in constraint_string.split(",")]
        self.lhs_variable.set_value(constraint[-1])
        for i in range(0, len(self.variables)):
            self.variables[i].set_value(constraint[i])
