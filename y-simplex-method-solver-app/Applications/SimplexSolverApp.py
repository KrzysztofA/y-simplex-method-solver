from View.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication

import sys


class SimplexSolverApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.app.exec()
