from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QWidget, QLabel, QVBoxLayout
from .StepTable import StepTable
from .OperationText import OperationText
from Model import ResultStruct
from typing import List


class WorkingOutView(QScrollArea):
    def __init__(self, parent=None, results: ResultStruct | None = None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.top_label = QLabel(parent=self)
        self.top_label.setWordWrap(True)
        self.top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.top_label)
        self.row_operations: List[OperationText] = []
        self.steps: List[StepTable] = []
        self.set_results(results)

    def set_results(self, results: ResultStruct | None):
        # Clean View
        self.clean()

        if results is None:
            self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.top_label.setText("This will show step-by-step working out once a solution is computed")

        if results is not None:
            self.top_label.setText("The following working out was computed:")
            temp_operations = [[av for ak, av in sorted(v.items(), key=lambda pair: pair[0])] for k, v in sorted(results.operations.items(), key=lambda pair: pair[0])]
            for i in range(0, len(temp_operations)):
                self.row_operations.append(OperationText(text="\n".join(temp_operations[i])))
            temp_steps = [[[bv for bk, bv in sorted(av.items(), key=lambda pair: pair[0])] for ak, av in sorted(v.items(), key=lambda pair: pair[0])] for k, v in sorted(results.steps.items(), key=lambda pair: pair[0])]
            for step in temp_steps:
                self.steps.append(StepTable(step))
            self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        for i in range(0, max(len(self.steps), len(self.row_operations))):
            if len(self.steps) > i:
                self.vbox.addWidget(self.steps[i])
            if len(self.row_operations) > i:
                self.vbox.addWidget(self.row_operations[i])

    def clean(self):
        for step in self.steps:
            self.vbox.removeWidget(step)
        for row in self.row_operations:
            self.vbox.removeWidget(row)
        self.steps = []
        self.row_operations = []
