from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from .VariableInputView import VariableInputView
from Model import ProblemType


class Function(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.z_label = QLabel("Z \u2264 ")
        self.layout.addWidget(self.z_label)
        self.setLayout(self.layout)
        self.vars  = []
        self.synchronize_variables(2)

    def set_problem(self, problem: ProblemType):
        if problem is ProblemType.Maximization:
            self.z_label.setText( "Z \u2264 " )
        elif problem is ProblemType.Minimization:
            self.z_label.setText( "Z \u2265 " )

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
        return_string += "1"
        return return_string