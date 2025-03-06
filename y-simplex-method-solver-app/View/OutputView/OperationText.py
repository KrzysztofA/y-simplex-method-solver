from PyQt6.QtWidgets import QLabel
from typing import List


class OperationText(QLabel):
    """
    A label that shows the operation text
    """
    def __init__(self, text=List[str], parent=None):
        super().__init__(parent)
        self.setWordWrap(True)

        # TODO Format text
        self.setText("".join(text))
