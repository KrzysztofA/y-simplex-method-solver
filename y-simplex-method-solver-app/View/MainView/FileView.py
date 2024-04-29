from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSpinBox, QPushButton, QComboBox
from View.InputView import InputBox
from View.OutputView import OutputBox
from Model import SimplexFile, ProblemType, FullSolutionStruct, ResultStruct, InputStruct
from Controller import o_parse_results, SettingsController, SimplexBackendController


class FileView(QWidget):
    def __init__(self, file: SimplexFile | None = None):
        super().__init__()
        self.last_solution = FullSolutionStruct("", {0: ""}, ResultStruct("", {0: ""}, {0: ""}))
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.output_box = OutputBox()
        self.grid_layout.addWidget(self.output_box, 0, 5, 1, 2)
        self.input_box = InputBox()
        self.grid_layout.addWidget(self.input_box, 0, 0, 1, 5)

        self.grid_layout.addWidget(QLabel("Variables No.:"), 1, 0)
        self.variable_number = QSpinBox()
        self.variable_number.setMinimum(1)
        self.variable_number.setValue(2)
        self.variable_number.valueChanged.connect(self.input_box.synchronize_variables)
        self.variable_number.valueChanged.connect(self.output_box.synchronize_variables)
        self.grid_layout.addWidget(self.variable_number, 1, 1)

        self.grid_layout.addWidget(QLabel("Constraint No.:"), 1, 2)
        self.constraint_number = QSpinBox()
        self.constraint_number.setMinimum(1)
        self.constraint_number.setValue(2)
        self.constraint_number.valueChanged.connect(self.input_box.set_constraints)
        self.grid_layout.addWidget(self.constraint_number, 1, 3)

        self.problem_type = QComboBox()
        self.problem_type.addItem("Maximization")
        self.problem_type.addItem("Minimization")
        self.problem_type.currentIndexChanged.connect(self.input_box.set_problem_int)
        self.problem_type.currentIndexChanged.connect(self.set_problem)
        self.grid_layout.addWidget(self.problem_type, 1, 4)

        self.problem = ProblemType.Maximization

        self.compute_button = QPushButton("Compute")
        self.grid_layout.addWidget(self.compute_button, 1, 5)
        self.compute_button.clicked.connect(self.compute_simplex)

        self.file_name: str = SettingsController().settings.default_save_name
        self.directory: str | None = None

        if file is not None:
            self.set_file(file)

    def collect_file(self):
        # Collect Input
        input_part = InputStruct(
            self.input_box.get_function(),
            {a[0]: a[1] for a in enumerate(self.input_box.get_constraints())},
            self.problem,
            self.variable_number.value(),
            self.constraint_number.value()
        )

        # Collect Output
        output_part = self.last_solution

        return SimplexFile(self.file_name, input_part, output_part, self.directory if self.directory is not None else "-1")

    def set_file(self, file: SimplexFile):
        self.last_solution = file.output
        self.problem = file.input.problem
        self.variable_number.setValue(file.input.variable_no)
        self.constraint_number.setValue(file.input.constraint_no)
        self.problem_type.setCurrentIndex(0 if file.input.problem == ProblemType.Maximization else 1)
        self.input_box.set_function(file.input.function_input)
        self.input_box.set_constraints_values(file.input.constraints)
        self.output_box.set_result(file.output.result.solution.split())
        self.file_name = file.filename
        self.directory = file.filedir

    def set_problem(self, problem: int):
        if problem == 0:
            self.problem = ProblemType.Maximization
        elif problem == 1:
            self.problem = ProblemType.Minimization

    def compute_simplex(self):
        self.last_solution.problem = self.problem
        SimplexBackendController().set_problem(self.last_solution.problem)
        SimplexBackendController().set_values(self.input_box.get_all_variables())
        result_raw = SimplexBackendController().collect_values()
        self.last_solution.result = o_parse_results(result_raw)
        self.output_box.set_result(self.last_solution.result.solution.split())
        self.last_solution.constraint_no = self.constraint_number.value()
        self.last_solution.variable_no = self.variable_number.value()
        self.last_solution.function = self.input_box.get_function()
        self.last_solution.constraints = {a[0]: a[1] for a in enumerate(self.input_box.get_constraints())}
