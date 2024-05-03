from enum import Enum
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from Model import ProblemType
from .NumberLineEdit import NumberLineEdit
from .VariableInputView import VariableInputView
from typing import List


class Sign(Enum):
    Equal = " = "
    Less = " \u2265 "
    Greater = " \u2264 "


class Function(QWidget):
    def __init__(self, variable_number: int = 2, constant_lhs_label: QWidget | None = None, parent: QWidget | None = None, maximization_sign: Sign = Sign.Equal, minimization_sign: Sign = Sign.Equal, problem_type: ProblemType = ProblemType.Maximization):
        super().__init__(parent)
        self.value_change_callbacks = None
        self.variable_number = variable_number
        self.maximization_sign: Sign = maximization_sign
        self.minimization_sign: Sign = minimization_sign
        self.variables: List[VariableInputView] = []
        self.setLayout(QHBoxLayout())
        self.lhs_variable: QWidget | None = None
        if constant_lhs_label is not None:
            self.lhs_variable = constant_lhs_label
            self.layout().addWidget(self.lhs_variable)
        else:
            self.lhs_variable: QWidget | None = NumberLineEdit()
            self.layout().addWidget(self.lhs_variable)
        self.equality_label = QLabel()
        self.set_problem(problem_type)
        self.layout().addWidget(self.equality_label)
        self.synchronize_variables(self.variable_number)

    def set_problem(self, problem: ProblemType):
        if problem is ProblemType.Maximization:
            self.equality_label.setText(f"{self.maximization_sign.value}")
        elif problem is ProblemType.Minimization:
            self.equality_label.setText(f"{self.minimization_sign.value}")

    def synchronize_variables(self, variable_number: int):
        if variable_number < len(self.variables):
            for i in self.variables[variable_number:]:
                self.layout().removeWidget(i)
                self.variables.remove(i)
        else:
            old_length = len(self.variables)
            for i in range(len(self.variables), variable_number):
                self.variables.append(VariableInputView(i, self))
            for i in range(old_length, len(self.variables)):
                self.layout().addWidget(self.variables[i])

    def get_variables_list(self):
        return_list = [self.lhs_variable.get_value() if isinstance(self.lhs_variable, NumberLineEdit) else '1']
        for i in self.variables:
            return_list.append(i.get_value())
        return return_list

    def get_variables_string(self):
        return_string = ""
        for i in self.variables:
            return_string += i.get_value() + ", "
        return_string += self.lhs_variable.get_value() if isinstance(self.lhs_variable, NumberLineEdit) else '1'
        return return_string

    def get_variables_float_list(self):
        return_list = [self.get_float(self.lhs_variable.get_value()) if isinstance(self.lhs_variable, NumberLineEdit) else 1]
        for i in self.variables:
            return_list.append(self.get_float(i.get_value()))
        return return_list

    @staticmethod
    def get_float(value_string):
        return float(value_string.split("/")[0]) / float(value_string.split("/")[1]) if "/" in value_string else float(
            value_string)
