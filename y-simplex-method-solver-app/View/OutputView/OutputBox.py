from PyQt6.QtWidgets import QWidget, QTabWidget, QSizePolicy
from .SolutionView import SolutionView
from .GraphOutputView import GraphOutputView


class OutputBox(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.solution_view = SolutionView(self)
        self.addTab(self.solution_view, "Solution View")
        self.graph_view = GraphOutputView(self)
        self.addTab(self.graph_view, "Graph View")
        self.addTab(QWidget(self), "Full Output View")
        self.functions_cache = []

    def synchronize_variables(self, var_no):
        self.solution_view.synchronize_variables(var_no)
        self.graph_view.synchronize_variables(var_no)

    def set_result(self, result: []):
        self.solution_view.set_result(result)
        self.graph_view.set_result(result)

    def set_view(self, index):
        self.setCurrentIndex(index)

    def pass_functions(self, functions):
        if len(self.functions_cache) == 0 or functions[0] != self.functions_cache[0] or sorted(functions[1:]) != sorted(self.functions_cache[1:]):
            self.functions_cache = functions
            self.graph_view.update_constraint_functions(functions[1:])
