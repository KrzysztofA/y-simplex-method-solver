from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout
from PyQt6.QtCore import Qt
from .VariableOutputView import VariableOutputView


class SolutionView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = QWidget(self)
        self.setWidget(self.widget)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        self.widget.setLayout(QVBoxLayout())
        self.z = VariableOutputView(-1)
        self.widget.layout().addWidget(self.z)
        self.vars = []
        self.synchronize_variables(2)

    def synchronize_variables(self, var_no):
        if var_no < len(self.vars):
            for i in self.vars[var_no:]:
                self.widget.layout().removeWidget(i)
                self.vars.remove(i)
        else:
            old_len = len(self.vars)
            for i in range(len(self.vars), var_no):
                self.vars.append(VariableOutputView(i))
            for i in range(old_len, len(self.vars)):
                self.widget.layout().addWidget(self.vars[i])

    def set_result(self, result: []):
        self.z.change_ans(result[0])
        for i in range(0, len(self.vars)):
            self.vars[i].change_ans(result[i + 1])
