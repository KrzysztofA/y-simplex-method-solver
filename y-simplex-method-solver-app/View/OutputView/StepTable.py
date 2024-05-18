from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget
from typing import Dict


class StepTable(QTableWidget):
    def __init__(self, step: Dict[str, int], parent: QWidget | None = None):
        super().__init__()
