import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, QSpinBox, QPushButton

from dotenv import load_dotenv
from View.MenuBar import MenuBar
from View.InputBox import InputBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.setWindowTitle(f'Simplex Method Solver by Yasuzume {os.getenv("YSIMPLEXMETHODSOLVERVER")}')
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout()
        self.main_widget.setLayout(self.layout)

        self.input_box = InputBox()
        self.layout.addWidget(self.input_box, 0, 0, 1, 4)

        self.layout.addWidget(QLabel("Variables No.:"), 1, 0)
        self.variable_number = QSpinBox()
        self.variable_number.setMinimum(1)
        self.variable_number.setValue(2)
        self.variable_number.valueChanged.connect(self.input_box.synchronize_variables)
        self.layout.addWidget(self.variable_number, 1, 1)

        self.layout.addWidget(QLabel("Constraint No.:"), 1, 2)
        self.constraint_number = QSpinBox()
        self.constraint_number.setMinimum(1)
        self.constraint_number.setValue(2)
        self.constraint_number.valueChanged.connect(self.input_box.set_constraints)
        self.layout.addWidget(self.constraint_number, 1, 3)

        self.layout.addWidget(QPushButton("Compute"))

        self.setMenuBar(MenuBar())
        self.show()
