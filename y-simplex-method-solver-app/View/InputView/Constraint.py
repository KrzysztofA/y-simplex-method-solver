from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from .NumberLineEdit import NumberLineEdit
from .VariableInputView import VariableInputView
from Model import ProblemType


class Constraint(QWidget):
    def __init__(self, var_no=2):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.equals = NumberLineEdit()
        self.eq_label = QLabel(" \u2265 ")
        self.layout.addWidget(self.equals)
        self.layout.addWidget(self.eq_label)
        self.vars = []
        self.synchronize_variables(var_no)

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
                self.vars.append(VariableInputView(i))
            for i in range(old_len, len(self.vars)):
                self.layout.addWidget(self.vars[i])

    def get_variables_string(self):
        return_string = ""
        for i in self.vars:
            return_string += i.get_value() + ", "
        return_string += self.equals.get_value()
        return return_string
