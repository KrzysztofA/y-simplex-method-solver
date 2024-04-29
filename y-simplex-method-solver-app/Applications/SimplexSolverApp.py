from PyQt6.QtWidgets import QFileDialog, QMessageBox

from Controller.SettingsController import SettingsController
from View import MainWindow, SettingsDialogue
from PyQt6.QtWidgets import QApplication
from Controller import SimplexBackendController, ToPDFConverter
from Controller import IOParser, ToDocumentConverter, ToHTMLConverter, SaveLoadController
from Model import FullSolutionStruct, ResultStruct, InputStruct, ProblemType

import sys
import os


def custom_export_factory(file_extensions):
    def custom_export(function):
        def wrapper(*args, **kwargs):
            dir_ = QFileDialog.getSaveFileName(None, 'Select a folder:',
                                               f'{args[0].settings_controller.default_save_path}', file_extensions)
            if dir_ is not None and dir_[0] != "":
                args[0].html_converter.set_problem(args[0].last_solution.problem)
                args[0].html_converter.set_constraints(args[0].last_solution.constraints)
                args[0].html_converter.set_equation(args[0].last_solution.function)
                if len(args[0].last_solution.result.solution) != 0:
                    args[0].html_converter.set_solution(args[0].last_solution.result.solution)
                if len(args[0].last_solution.result.steps) != 0:
                    args[0].html_converter.set_steps(args[0].last_solution.result.steps)
                    args[0].html_converter.set_variable_no(args[0].last_solution.variable_no)
                    args[0].html_converter.set_constraints_no(args[0].last_solution.constraint_no)
                    args[0].html_converter.set_operations(args[0].last_solution.result.operations)
                kwargs["directory"] = dir_[0]
                function(args[0], **kwargs)
                args[0].settings_controller.auto_set_default_save_path(dir_[0])

        return wrapper

    return custom_export


class SimplexSolverApp:
    def __init__(self):
        # Entry point needs to be QApplication
        self.app = QApplication(sys.argv)

        # Controller
        self.simplex_backend = SimplexBackendController()
        self.html_converter = ToHTMLConverter()
        self.doc_converter = ToDocumentConverter()
        self.pdf_converter = ToPDFConverter()
        self.save_load_controller = SaveLoadController()

        self.settings_controller = SettingsController()

        # Variables
        self.last_solution = FullSolutionStruct("", {0: ""}, ResultStruct("", {0: ""}, {0: ""}))
        self.files = [self.settings_controller.settings.default_save_name]
        self.current_index = 0

        # View
        self.main_window = MainWindow()
        self.settings_dialogue = SettingsDialogue(self.settings_controller)

        # Stream from View To Controller
        self.main_window.compute_button.clicked.connect(self.compute_simplex)
        self.main_window.menu_bar.to_html_action.triggered.connect(self.save_to_html_file)
        self.main_window.menu_bar.to_doc_action.triggered.connect(self.save_to_document_file)
        self.main_window.menu_bar.to_pdf_action.triggered.connect(self.save_to_pdf_file)
        self.main_window.menu_bar.settings_action.triggered.connect(self.settings_dialogue.exec)
        self.main_window.menu_bar.save_action.triggered.connect(self.save_or_save_as)
        self.main_window.menu_bar.save_as_action.triggered.connect(self.save_as)
        self.main_window.menu_bar.load_action.triggered.connect(self.load_file)

        # App Call
        self.app.exec()

    def compute_simplex(self):
        self.last_solution.problem = self.main_window.problem
        self.simplex_backend.set_problem(self.last_solution.problem)
        self.simplex_backend.set_values(self.main_window.input_box.get_all_variables())
        self.simplex_backend.collect_steps = True
        result_raw = self.simplex_backend.collect_values()
        self.last_solution.result = IOParser.o_parse_results(result_raw)
        self.main_window.output_box.set_result(self.last_solution.result.solution.split())
        self.last_solution.constraint_no = self.main_window.constraint_number.value()
        self.last_solution.variable_no = self.main_window.variable_number.value()
        self.last_solution.function = self.main_window.input_box.get_function()
        self.last_solution.constraints = {a[0]: a[1] for a in enumerate(self.main_window.input_box.get_constraints())}

    @custom_export_factory(file_extensions="HTML Files (*.html)")
    def save_to_html_file(self, directory):
        self.html_converter.save_as_html(directory)

    @custom_export_factory(file_extensions="Document Files (*.docx *.rtf *.doc *.docm *.odt)")
    def save_to_document_file(self, directory):
        self.doc_converter.set_lines(self.html_converter.convert())
        self.doc_converter.save_as_document(directory)

    @custom_export_factory(file_extensions="PowerPoint Files (*.pdf)")
    def save_to_pdf_file(self, directory):
        self.pdf_converter.set_lines(self.html_converter.convert())
        self.pdf_converter.save_as_pdf(directory)

    def save_as(self):
        save_path = f'{self.settings_controller.default_save_path}'
        if os.path.isfile(self.files[self.current_index]):
            save_path = f'{self.files[self.current_index]}'

        dir_ = QFileDialog.getSaveFileName(None, 'Select a folder:', save_path,
                                           "Simplex Solver File (*.yse)")
        if dir_ is not None and dir_[0] != "":
            self.save_file(dir_[0])

    def save_or_save_as(self):
        save_path = f'{self.settings_controller.default_save_path}'
        if os.path.isfile(self.files[self.current_index]):
            self.save_file(self.files[self.current_index])
        else:
            self.save_as()

    def save_file(self, directory):
        if directory != "":

            # Collect Input
            input_part = InputStruct(
                self.main_window.input_box.get_function(),
                {a[0]: a[1] for a in enumerate(self.main_window.input_box.get_constraints())},
                self.main_window.problem,
                self.main_window.variable_number.value(),
                self.main_window.constraint_number.value()
            )

            # Collect Output
            output_part = self.last_solution

            self.save_load_controller.set_input_data(input_part)
            self.save_load_controller.set_output_data(output_part)
            self.save_load_controller.save(directory)

    def load_file(self):
        dir_ = QFileDialog.getOpenFileName(None, 'Select a file:',
                                           f'{self.settings_controller.settings.default_save_dir}',
                                           "Simplex Solver File (*.yse)")
        if dir_ is not None and dir_[0] != "":
            try:
                loaded_file = self.save_load_controller.load(dir_[0])
                loaded_file.output.problem = loaded_file.output.problem
                self.last_solution = loaded_file.output
                self.main_window.variable_number.setValue(loaded_file.input.variable_no)
                self.main_window.constraint_number.setValue(loaded_file.input.constraint_no)
                self.main_window.problem_type.setCurrentIndex(0 if loaded_file.input.problem == ProblemType.Maximization else 1)
                self.main_window.input_box.set_function(loaded_file.input.function_input)
                self.main_window.input_box.set_constraints_values(loaded_file.input.constraints)
                self.main_window.output_box.set_result(self.last_solution.result.solution.split())
            except Exception:
                QMessageBox.critical(self.main_window, "Error", "Failed to load file, file may be corrupted")


if __name__ == '__main__':
    app = SimplexSolverApp()
