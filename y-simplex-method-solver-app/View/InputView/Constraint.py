from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication
from .NumberLineEdit import NumberLineEdit
from .VariableInputView import VariableInputView
from Model import ProblemType


class Constraint(QWidget):
    def __init__(self, parent=None, var_no=2, problem=ProblemType.Maximization):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.equals = NumberLineEdit(parent)
        self.eq_label = QLabel(f" {"\u2265" if problem == ProblemType.Maximization else "\u2264"} ")
        self.layout.addWidget(self.equals)
        self.layout.addWidget(self.eq_label)
        self.vars = []
        self.synchronize_variables(var_no)
        self.value_change_callbacks = []

    def set_problem(self, problem: ProblemType):
        if problem is ProblemType.Maximization:
            self.eq_label.setText(" \u2265 ")
        elif problem is ProblemType.Minimization:
            self.eq_label.setText(" \u2264 ")

    def synchronize_variables(self, var_no: int):
        if var_no < len(self.vars):
            for i in self.vars[var_no:]:
                self.layout.removeWidget(i)
                self.vars.remove(i)
        else:
            old_len = len(self.vars)
            for i in range(len(self.vars), var_no):
                self.vars.append(VariableInputView(i, self.parentWidget()))
            for i in range(old_len, len(self.vars)):
                self.layout.addWidget(self.vars[i])

    def get_variables_list(self):
        return_list = [self.equals.get_value()]
        for i in self.vars:
            return_list.append(i.get_value())
        for a in self.value_change_callbacks:
            a(return_list)
        return return_list

    def get_variables_string(self):
        return_string = ""
        for i in self.vars:
            return_string += i.get_value() + ", "
        return_string += self.equals.get_value()
        return return_string

    def set_values_from_string(self, constraint_string: str):
        constraint = [a.strip() for a in constraint_string.split(",")]
        self.equals.set_value(constraint[-1])
        for i in range(0, len(self.vars)):
            self.vars[i].set_value(constraint[i])
