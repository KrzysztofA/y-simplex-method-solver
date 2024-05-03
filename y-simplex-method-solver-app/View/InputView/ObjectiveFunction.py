from PyQt6.QtWidgets import QWidget, QLabel
from .Function import Function


class ObjectiveFunction(Function):
    def __init__(self, parent: QWidget | None = None, variable_number: int = 2):
        super().__init__(variable_number, QLabel("Z"), parent)

    def set_variables_from_string(self, function_string: str):
        function = [a.strip() for a in function_string.split(",")]
        for i in range(0, len(self.variables)):
            self.variables[i].set_value(function[i])
