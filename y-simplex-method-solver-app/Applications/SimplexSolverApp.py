from PyQt6.QtWidgets import QFileDialog

from View.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
from Controller import SimplexBackendController, ToPDFConverter
from Controller import IOParser, ToDocumentConverter, ToHTMLConverter
from Model import FullSolutionStruct, ResultStruct

import sys
import os


class SimplexSolverApp:
    def __init__(self):
        # Entry point needs to be QApplication
        self.app = QApplication(sys.argv)

        # Variables
        self.last_solution = FullSolutionStruct([], [], ResultStruct([], []))

        # Controller
        self.simplex_backend = SimplexBackendController()
        self.html_converter = ToHTMLConverter()
        self.doc_converter = ToDocumentConverter()
        self.pdf_converter = ToPDFConverter()

        # View
        self.main_window = MainWindow()

        # Stream from View To Controller
        self.main_window.compute_button.clicked.connect(self.compute_simplex)
        self.main_window.menu_bar.to_html_action.triggered.connect(self.save_to_html_file)
        self.main_window.menu_bar.to_doc_action.triggered.connect(self.save_to_document_file)
        self.main_window.menu_bar.to_pdf_action.triggered.connect(self.save_to_pdf_file)

        # App Call
        self.app.exec()

    def compute_simplex(self):
        self.last_solution.problem = self.main_window.problem
        self.simplex_backend.set_problem(self.last_solution.problem)
        self.simplex_backend.set_values(self.main_window.input_box.get_all_variables())
        self.simplex_backend.collect_steps = True
        result_raw = self.simplex_backend.collect_values()
        self.last_solution.result = IOParser.o_parse_results(result_raw)
        self.main_window.output_box.set_result(self.last_solution.result.solution)
        self.last_solution.constraint_no = self.main_window.constraint_number.value()
        self.last_solution.variable_no = self.main_window.variable_number.value()
        self.last_solution.function = self.main_window.input_box.get_function().split(",")
        self.last_solution.constraints = self.main_window.input_box.get_constraints()

    def save_to_html_file(self):
        dir_ = QFileDialog.getSaveFileName(None, 'Select a folder:', 'C:\\New Simplex Solution', "HTML Files (*.html)")
        if dir_ is not None and dir_[0] != "":
            self.set_html_converter()
            self.html_converter.save_as_html(dir_[0])

    def save_to_document_file(self):
        dir_ = QFileDialog.getSaveFileName(None, 'Select a folder:', 'C:\\New Simplex Solution', "Document Files (*.docx *.rtf *.doc *.docm *.odt)")
        if dir_ is not None and dir_[0] != "":
            self.set_html_converter()
            self.doc_converter.set_lines(self.html_converter.convert())
            self.doc_converter.save_as_document(dir_[0])

    def save_to_pdf_file(self):
        dir_ = QFileDialog.getSaveFileName(None, 'Select a folder:', 'C:\\New Simplex Solution', "PowerPoint Files (*.pdf)")
        if dir_ is not None and dir_[0] != "":
            self.set_html_converter()
            self.pdf_converter.set_lines(self.html_converter.convert())
            self.pdf_converter.save_as_pdf(dir_[0])

    def set_html_converter(self):
        self.html_converter.set_problem(self.last_solution.problem)
        self.html_converter.set_constraints(self.last_solution.constraints)
        self.html_converter.set_equation(self.last_solution.function)
        if len(self.last_solution.result.solution) != 0:
            self.html_converter.set_solution(self.last_solution.result.solution)
        if len(self.last_solution.result.steps) != 0:
            self.html_converter.set_steps(self.last_solution.result.steps)
            self.html_converter.variable_no = self.last_solution.variable_no
            self.html_converter.constraints_no = self.last_solution.constraint_no


if __name__ == '__main__':
    app = SimplexSolverApp()
