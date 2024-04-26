from PyQt6.QtWidgets import QFileDialog

from View.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
from Controller import SimplexBackendController
from Controller import IOParser, ToHTMLConverter

import sys


class SimplexSolverApp:
    def __init__(self):
        # Variables
        self.result = []

        # Controller
        self.simplex_backend = SimplexBackendController()
        self.html_converter = ToHTMLConverter()

        # View
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

        # Stream from View To Controller
        self.main_window.compute_button.clicked.connect(self.set_backend)
        self.main_window.menu_bar.to_html_action.triggered.connect(self.save_to_html_file)

        # App Call
        self.app.exec()

    def set_backend(self):
        self.simplex_backend.set_problem(self.main_window.problem)
        self.simplex_backend.set_values(self.main_window.input_box.get_all_variables())
        result_raw = self.simplex_backend.collect_values()
        self.result = IOParser.o_parse_to_arr(result_raw)
        self.main_window.output_box.set_result(self.result)

    def save_to_html_file(self):
        self.html_converter.set_problem(self.main_window.problem)
        self.html_converter.set_constraints(self.main_window.input_box.get_constraints())
        self.html_converter.set_equation(self.main_window.input_box.get_function().split(","))
        if len(self.result) != 0:
            self.html_converter.set_solution(self.result)
        dir_ = QFileDialog.getSaveFileName(None, 'Select a folder:', 'C:\\', "HTML Files (*.html)")
        if dir_ != "":
            self.html_converter.save_as_html(dir_[0])


if __name__ == '__main__':
    app = SimplexSolverApp()
