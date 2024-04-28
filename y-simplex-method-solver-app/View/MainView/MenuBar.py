from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QIcon


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        file_menu = self.addMenu("&File")
        edit_menu = self.addMenu("&Edit")
        self.addSeparator()
        help_menu = self.addMenu("&Help")
        file_menu.addAction("&New")
        self.save_action = file_menu.addAction("&Save")
        self.save_as_action = file_menu.addAction("&Save As")
        self.load_action = file_menu.addAction("Load")
        file_menu.addSeparator()
        export_menu = file_menu.addMenu("&Export")
        self.to_doc_action = export_menu.addAction(QIcon(), "&To Document")
        self.to_pdf_action = export_menu.addAction("&To PDF")
        self.to_html_action = export_menu.addAction("&To HTML")
        edit_menu.addAction("&Undo")
        edit_menu.addAction("&Redo")
        edit_menu.addSeparator()
        self.settings_action = edit_menu.addAction("&Settings")
        help_menu.addAction("Instruction")
        help_menu.addSeparator()
        help_menu.addAction("About")
        help_menu.addAction("Credits")
        help_menu.addAction("Contact")
