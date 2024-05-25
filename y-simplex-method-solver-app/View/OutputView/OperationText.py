from PyQt6.QtWidgets import QLabel
from typing import List


class OperationText(QLabel):
    def __init__(self, text=List[str], parent=None):
        super().__init__(parent)
        self.setWordWrap(True)

        # TODO Format text
        self.text = "\n".join(text)
