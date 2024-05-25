from PyQt6.QtWidgets import QTableWidget, QWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from typing import List


class StepTable(QTableWidget):
    def __init__(self, step: List[List[str]], parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.setRowCount(len(step))
        self.setColumnCount(len(step[0]))
        for row in range(len(step)):
            for col in range(len(step[row])):
                self.setItem(row, col, QTableWidgetItem(step[row][col]))
