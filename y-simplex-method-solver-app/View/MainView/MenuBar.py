from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QIcon


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        
        # Set Menus
        file_menu = self.addMenu("&File")
        edit_menu = self.addMenu("&Edit")
        # view_menu = self.addMenu("&View")
        help_menu = self.addMenu("&Help")
        
        # File Menu Actions
        self.new_action = file_menu.addAction("&New")
        self.save_action = file_menu.addAction("&Save")
        self.save_as_action = file_menu.addAction("&Save As")
        self.load_action = file_menu.addAction("Load")
        file_menu.addSeparator()
        export_menu = file_menu.addMenu("&Export")
        self.to_doc_action = export_menu.addAction(QIcon(), "&To Document")
        self.to_pdf_action = export_menu.addAction("&To PDF")
        self.to_html_action = export_menu.addAction("&To HTML")
        
        # Edit Menu Actions
        all_files_action = edit_menu.addMenu("&All Files Action")
        self.set_variables_output = all_files_action.addAction("&Set Variables Output")
        self.set_graph_output = all_files_action.addAction("&Set Graph Output")
        self.set_working_output = all_files_action.addAction("&Set Working Out Output")
        edit_menu.addSeparator()
        self.settings_action = edit_menu.addAction("&Settings")
        
        # View Menu Actions
        self.workspace_view = view_menu.addAction("&Workspace")
        self.workspace_view.setCheckable(True)
        self.workspace_view.setChecked(True)
        output_view = view_menu.addMenu("&Output")
        self.graph_view = output_view.addAction("&Graph")
        self.graph_view.setCheckable(True)
        self.graph_view.setChecked(True)
        self.working_view = output_view.addAction("&Work Out")
        self.working_view.setCheckable(True)
        self.working_view.setChecked(True)
        
        # Help Menu Actions
        self.instruction_action = help_menu.addAction("&Instruction")
        help_menu.addSeparator()
        self.about_action = help_menu.addAction("&About")
        # help_menu.addAction("Credits")
