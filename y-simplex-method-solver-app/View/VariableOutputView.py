from PyQt6.QtWidgets import QLabel


class VariableOutputView(QLabel):
    def __init__(self, no: int, ans: str = "?"):

        if no != -1:
            super().__init__(f"x{no} = {ans}")
        else:
            super().__init__(f"Z = {ans}")
