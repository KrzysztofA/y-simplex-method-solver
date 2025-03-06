from PyQt6.QtWidgets import QLabel


class VariableOutputView(QLabel):
    """
    Shows a variable output in the form of x1 = 5 or Z = 5. 
    If the number is -1, it will show Z instead of x{number}.
    """
    def __init__(self, no: int, ans: str = "?"):
        self.number = no
        if self.number != -1:
            super().__init__(f"x{self.number} = {ans}")
        else:
            super().__init__(f"Z = {ans}")

    def change_ans(self, ans: str):
        """
        Changes the answer of the variable output
        :param ans: The new answer
        """
        if self.number != -1:
            self.setText(f"x{self.number} = {ans}")
        else:
            self.setText(f"Z = {ans}")
