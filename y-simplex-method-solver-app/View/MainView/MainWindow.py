import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, QSpinBox, QPushButton, QComboBox, QMenuBar

from dotenv import load_dotenv
from View.MainView import MenuBar
from View.InputView import InputBox
from View.OutputView import OutputBox
from Model.ProblemType import ProblemType


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.setWindowTitle(f'Simplex Method Solver by Yasuzume {os.getenv("YSIMPLEXMETHODSOLVERVER", "Unversioned")}')
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout()
        self.main_widget.setLayout(self.layout)
        self.output_box = OutputBox()
        self.layout.addWidget(self.output_box, 0, 5, 1, 2)
        self.input_box = InputBox()
        self.layout.addWidget(self.input_box, 0, 0, 1, 5)

        self.layout.addWidget(QLabel("Variables No.:"), 1, 0)
        self.variable_number = QSpinBox()
        self.variable_number.setMinimum(1)
        self.variable_number.setValue(2)
        self.variable_number.valueChanged.connect(self.input_box.synchronize_variables)
        self.variable_number.valueChanged.connect(self.output_box.synchronize_variables)
        self.layout.addWidget(self.variable_number, 1, 1)

        self.layout.addWidget(QLabel("Constraint No.:"), 1, 2)
        self.constraint_number = QSpinBox()
        self.constraint_number.setMinimum(1)
        self.constraint_number.setValue(2)
        self.constraint_number.valueChanged.connect(self.input_box.set_constraints)
        self.layout.addWidget(self.constraint_number, 1, 3)

        self.problem_type = QComboBox()
        self.problem_type.addItem("Maximization")
        self.problem_type.addItem("Minimization")
        self.problem_type.currentIndexChanged.connect(self.input_box.set_problem_int)
        self.problem_type.currentIndexChanged.connect(self.set_problem)
        self.layout.addWidget(self.problem_type, 1, 4)

        self.problem = ProblemType.Maximization

        self.compute_button = QPushButton("Compute")
        self.layout.addWidget(self.compute_button, 1, 5)

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)
        self.show()

    def set_problem(self, problem: int):
        if problem == 0:
            self.problem = ProblemType.Maximization
        elif problem == 1:
            self.problem = ProblemType.Minimization
