from PyQt6.QtWidgets import QMessageBox, QDialogButtonBox
from PyQt6.QtCore import Qt


class ContactView(QMessageBox):
    """
    Class used to display contact information
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.setWindowTitle("About")
        self.setTextFormat(Qt.TextFormat.RichText)
        self.setText("Application used to solve Optimization (Maximization/Minimization) Problem<br/>by Krzysztof "
                     "Siatkowski<br/><a href='mailto:krzysztof.a.siatkowski@gmail.com'>Email Me</a>")
        self.setStandardButtons(QMessageBox.StandardButton.Close)
