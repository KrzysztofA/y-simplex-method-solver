from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class InstructionView(QDialog):
    """
    A class used to display instructions on how to use the application
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instructions")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("Instructions")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label = QLabel("1. In the bottom row, enter the number of variables and constraints\n"
                           "2. Enter the coefficients of the objective function\n"
                           "3. Enter the coefficients of the constraints\n"
                           "4. Select the type of optimization problem\n"
                           "5. Click the Compute button\n"
                           "6. The solution and any working out will be displayed in the window on the right")
        self.label.setWordWrap(True)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.label)
