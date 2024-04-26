from PyQt6.QtWidgets import QLabel


class VariableOutputView(QLabel):
    def __init__(self, no: int, ans: str = "?"):
        self.number = no
        if self.number != -1:
            super().__init__(f"x{self.number} = {ans}")
        else:
            super().__init__(f"Z = {ans}")

    def change_ans(self, ans: str):
        if self.number != -1:
            self.setText(f"x{self.number} = {ans}")
        else:
            self.setText(f"Z = {ans}")

