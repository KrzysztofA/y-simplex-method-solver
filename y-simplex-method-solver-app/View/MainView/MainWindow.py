import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, QSpinBox, QPushButton, QComboBox, QTabWidget

from dotenv import load_dotenv
from View.MainView import MenuBar
from View.InputView import InputBox
from View.OutputView import OutputBox
from .FileView import FileView
from Model.ProblemType import ProblemType
from .FileTabBar import FileTabBar
from Controller import SettingsController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.setWindowTitle(f'Simplex Method Solver by Yasuzume {os.getenv("YSIMPLEXMETHODSOLVERVER", "Unversioned")}')
        self.main_widget = QWidget()
        self.tab_bar = FileTabBar()
        self.tab_bar.add_new_file()
        self.tab_bar.setCurrentIndex(0)
        self.current_tab_index = 0

        self.setCentralWidget(self.tab_bar)

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)
        self.show()

    def current_file(self):
        return self.tab_bar.current_file()
