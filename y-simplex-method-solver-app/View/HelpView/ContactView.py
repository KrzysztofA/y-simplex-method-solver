from PyQt6.QtWidgets import QMessageBox, QDialogButtonBox


class ContactView(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.setWindowTitle("About")
        self.setText("Application used to solve Optimization (Maximization/Minimization) Problem\nby Krzysztof "
                     "Siatkowski")
