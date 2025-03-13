import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QSplitter

from dotenv import load_dotenv
from View.MainView import MenuBar
from .FileTabBar import FileTabBar
from View.DirectoryView import WorkingDirectoryView, DirectoryViewWidget


class MainWindow(QMainWindow):
    """
    Main Window of the application
    """
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.setWindowTitle(f'Simplex Method Solver by Yasuzume {os.getenv("YSIMPLEXMETHODSOLVERVER", "Unversioned")}')
        self.main_widget = QSplitter()
        self.folder_view = DirectoryViewWidget()
        self.tab_bar = FileTabBar()
        self.tab_bar.add_new_file()
        self.tab_bar.setCurrentIndex(0)
        self.current_tab_index = 0

        self.main_widget.addWidget(self.folder_view)
        self.main_widget.addWidget(self.tab_bar)
        self.main_widget.setCollapsible(0, False)
        self.main_widget.setCollapsible(1, False)

        self.setCentralWidget(self.main_widget)

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)
        self.show()

    def current_file(self):
        """
        Get the current file
        """
        return self.tab_bar.current_file()
