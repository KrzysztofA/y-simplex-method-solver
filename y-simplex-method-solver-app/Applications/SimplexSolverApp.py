from View.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
from Controller import SimplexBackendController
from Controller import IOParser

import sys


class SimplexSolverApp:
    def __init__(self):
        # Controller
        self.simplex_backend = SimplexBackendController()

        # View
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

        # Stream from View To Controller
        def set_backend():
            self.simplex_backend.set_problem(self.main_window.problem)
            self.simplex_backend.set_values(self.main_window.input_box.get_all_variables())
            result = IOParser.o_parse_to_arr(self.simplex_backend.collect_values())
            self.main_window.output_box.set_result(result)

        self.main_window.compute_button.clicked.connect(set_backend)

        # App Call
        self.app.exec()
