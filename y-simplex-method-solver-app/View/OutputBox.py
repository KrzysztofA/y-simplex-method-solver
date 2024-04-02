from PyQt6.QtWidgets import QScrollArea, QFrame


class OutputBox(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
