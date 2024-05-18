from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QWidget, QLabel, QVBoxLayout
from .StepTable import StepTable
from Model import ResultStruct
from typing import List


class WorkingOutView(QScrollArea):
    def __init__(self, parent=None, results: ResultStruct | None = None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.top_label = QLabel(self)
        self.top_label.setWordWrap(True)
        self.top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.top_label)
        self.row_operations: List[QLabel] = []
        self.steps: List[StepTable] = []
        self.set_results(results)

    def set_results(self, results: ResultStruct | None):
        if results is None:
            self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.top_label.setText("This will show step-by-step working out once a solution is computed")

        if results is not None:
            self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.top_label.setText("The following working out was computed:")
            print(results)
            for i in range(0, len(results.operations)):
                print(results.operations[i])
                self.row_operations.append(QLabel(results.operations[i]))
            for index, step in sorted(list(results.steps), key=lambda x: int(x.key)):
                for row_index, row in sorted(list(step), key=lambda x: int(x.key)):
                    print(row)
                    self.vbox.addWidget(StepTable(step))

        for i in range(0, max(len(self.steps), len(self.row_operations))):
            if len(self.row_operations) > i:
                self.vbox.addWidget(self.row_operations[i])
            if len(self.steps) > i:
                self.vbox.addWidget(self.steps[i])
