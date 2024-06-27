from PyQt6.QtWidgets import QFileDialog, QMessageBox, QStyle, QStyleFactory, QProxyStyle
from PyQt6.QtCore import Qt

from Controller.SettingsController import SettingsController
from Model import SimplexFile
from View import MainWindow, SettingsDialogue
from PyQt6.QtWidgets import QApplication
from Controller import SimplexBackendController, ToPDFConverter
from Controller import ToDocumentConverter, ToHTMLConverter, SaveLoadController

import sys
import os

from View.HelpView import ContactView


def custom_export_factory(file_extensions):
    def custom_export(function):
        def wrapper(*args, **kwargs):
            current_file = args[0].main_window.current_file()
            if current_file is False:
                QMessageBox.critical(args[0].main_window, "Error", "Please select a file.")
                return
            dir_ = QFileDialog.getSaveFileName(None, 'Select a folder:',
                                               f'{SettingsController().default_save_path}', file_extensions)
            if dir_ is not None and dir_[0] != "":
                current_file = args[0].main_window.current_file()
                last_solution = current_file.last_solution
                html_converter = args[0].html_converter
                html_converter.set_problem(last_solution.problem)
                html_converter.set_constraints(last_solution.constraints)
                html_converter.set_equation(last_solution.function)
                if len(last_solution.result.solution) != 0:
                    html_converter.set_solution(last_solution.result.solution)
                if len(last_solution.result.steps) != 0:
                    html_converter.set_steps(last_solution.result.steps)
                    html_converter.set_variable_no(last_solution.variable_no)
                    html_converter.set_constraints_no(last_solution.constraint_no)
                    html_converter.set_operations(last_solution.result.operations)
                kwargs["directory"] = dir_[0]
                function(args[0], **kwargs)
                SettingsController().auto_set_default_save_path(dir_[0])

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

        # Views
        self.main_window = MainWindow()
        self.main_window.setMinimumSize(640, 420)
        self.main_window.folder_view.working_directory_view.open_file_callbacks.append(self.open_file)
        self.settings_dialogue = SettingsDialogue()
        self.about_dialogue = ContactView()

        # Stream from View To Controller
        self.main_window.menu_bar.new_action.triggered.connect(self.main_window.tab_bar.add_new_file)
        self.main_window.menu_bar.to_html_action.triggered.connect(self.save_to_html_file)
        self.main_window.menu_bar.to_doc_action.triggered.connect(self.save_to_document_file)
        self.main_window.menu_bar.to_pdf_action.triggered.connect(self.save_to_pdf_file)
        self.main_window.menu_bar.settings_action.triggered.connect(self.settings_dialogue.exec)
        self.main_window.menu_bar.about_action.triggered.connect(self.about_dialogue.exec)
        self.main_window.menu_bar.save_action.triggered.connect(self.save_or_save_as)
        self.main_window.menu_bar.save_as_action.triggered.connect(self.save_as)
        self.main_window.menu_bar.load_action.triggered.connect(self.load_file)
        self.main_window.menu_bar.set_variables_output.triggered.connect(lambda: self.main_window.tab_bar.set_all_view(0))
        self.main_window.menu_bar.set_graph_output.triggered.connect(lambda: self.main_window.tab_bar.set_all_view(1))
        self.main_window.menu_bar.set_working_output.triggered.connect(lambda: self.main_window.tab_bar.set_all_view(2))

        # App Call
        self.app.exec()

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
        if not self.main_window.current_file():
            QMessageBox.warning(self.main_window, 'Warning', 'No file selected.')
            return
        save_path = f'{SettingsController().default_save_path}'
        if self.main_window.current_file().directory is not None and os.path.isfile(self.main_window.current_file().directory):
            save_path = f'{self.main_window.current_file().directory}'

        dir_ = QFileDialog.getSaveFileName(None, 'Select a folder:', save_path,
                                           "Simplex Solver File (*.yse)")
        if dir_ is not None and dir_[0] != "":
            self.main_window.current_file().directory = dir_[0]
            self.save_file(dir_[0])

    def save_or_save_as(self):
        if not self.main_window.current_file():
            QMessageBox.warning(self.main_window, 'Warning', 'No file selected.')
            return
        if self.main_window.current_file().directory is not None and os.path.isfile(self.main_window.current_file().directory):
            self.save_file(self.main_window.current_file().directory)
        else:
            self.save_as()

    def save_file(self, directory):
        if directory != "":
            # Collect
            file = self.main_window.tab_bar.collect_current_file()

            # Save
            SaveLoadController().save(directory, file)
            self.main_window.tab_bar.set_current_file(file)

    def load_file(self):
        dir_ = QFileDialog.getOpenFileName(None, 'Select a file:',
                                           f'{SettingsController().settings.default_save_dir}',
                                           "Simplex Solver File (*.yse)")
        if dir_ is not None and dir_[0] != "":
            try:
                self.open_file(SaveLoadController().load(dir_[0]))
            except Exception:
                QMessageBox.critical(self.main_window, "Error", "Failed to load file, file may be corrupted")

    def open_file(self, loaded_file: SimplexFile):
        if SettingsController().settings.open_in_new_tab:
            self.main_window.tab_bar.add_file(loaded_file)
        else:
            self.main_window.tab_bar.set_current_file(loaded_file)


if __name__ == '__main__':
    app = SimplexSolverApp()
