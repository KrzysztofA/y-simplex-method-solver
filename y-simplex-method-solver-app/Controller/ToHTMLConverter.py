from typing import List

from Model import ProblemType


class ToHTMLConverter:
    def __init__(self):
        self.problem_type: ProblemType = ProblemType.Maximization
        self.equation: List[str] = []
        self.constraints: List[str] = []
        self.steps: List[str] = []
        self.solution: List[str] = []

    def set_equation(self, equation: List[str]):
        self.equation = [a.strip() for a in equation]

    def set_constraints(self, constraints: List[str]):
        self.constraints = constraints

    def set_steps(self, steps: List[str]):
        self.steps = steps

    def set_solution(self, solution: List[str]):
        self.solution = [a.strip() for a in solution]

    def set_problem(self, problem_type: ProblemType):
        self.problem_type = problem_type

    @staticmethod
    def value_format(value: str, all_values: bool = False) -> str:
        return f"{"&frasl;".join([a for a in value.split("/")]) if "/" in value else value if value != "1" and value != "0" or all_values else ""}"

    @staticmethod
    def variable_format(value: str, index: int):
        return f"x<sub>{index}</sub>" if value != "0" else ""

    @staticmethod
    def all_but_last_format(char: str, value: str, index: int, max_index: int, all_values: bool = False) -> str:
        return "" if all_values is False and value == "0" or index == max_index else f"{char}"

    def convert(self):
        lines = []
        function_delim = "<" if self.problem_type == ProblemType.Maximization else ">"
        lines.append(
            f"<p>{"Maximize" if self.problem_type == ProblemType.Maximization else "Minimize"} the following equation:</p>")
        lines.append(
            f"<p>Z {function_delim} {"".join([f"{self.value_format(value)}{self.variable_format(value, index)}{self.all_but_last_format(" + ", value, index, len(self.equation) - 2)}" for index, value in enumerate(self.equation[:-1])])}</p>")
        lines.append("<p>Subject to constraints:</p>")
        lines.append("<p>")
        for i in self.constraints:
            i_arr = [a.strip() for a in i.split(",")]
            lines.append(
                f"<div>  {"".join([f"{self.value_format(value)}{self.variable_format(value, index)}{self.all_but_last_format(" + ", value, index, len(i_arr) - 1)}" for index, value in enumerate(i_arr[:-1])])} {function_delim} {self.value_format(i_arr[-1], True)}</div>")
        lines.append("</p>")
        if len(self.steps) != 0:
            pass
        if len(self.solution) != 0:
            lines.append("<p>After the computation, the following results were obtained:</p>")
            lines.append(
                f"<p>Z = {self.value_format(self.solution[0], True)}, {" ".join([f"x<sub>{index}</sub> = {self.value_format(value, True)}{self.all_but_last_format(",", value, index, len(self.solution) - 2, True)}" for index, value in enumerate(self.solution[1:])])}</p>")
        return lines

    def save_as_html(self, path: str):
        lines = self.convert()
        with open(path, "w") as file:
            for line in lines:
                file.write(line)
