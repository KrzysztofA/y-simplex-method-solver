from typing import List

from Model import ProblemType


class ToHTMLConverter:
    def __init__(self):
        self.problem_type: ProblemType = ProblemType.Maximization
        self.equation: List[str] = []
        self.constraints: List[str] = []
        self.solution: List[str] = []

        # Steps only vars
        self.steps: List[str] = []
        self.variable_no: int = 0
        self.constraints_no: int = 0

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
                f"<div>{"".join([f"{self.value_format(value)}{self.variable_format(value, index)}{self.all_but_last_format(" + ", value, index, len(i_arr) - 1)}" for index, value in enumerate(i_arr[:-1])])} {function_delim} {self.value_format(i_arr[-1], True)}</div>")
        lines.append("</p>")
        if len(self.steps) != 0:
            for i in range(0, len(self.steps)):
                lines.extend(self.build_step_table(i))
        if len(self.solution) != 0:
            lines.append("<p>After the computation, the following results were obtained:</p>")
            lines.append(
                f"<p>Z = {self.value_format(self.solution[0], True)}, {" ".join([f"x<sub>{index}</sub> = {self.value_format(value, True)}{self.all_but_last_format(",", value, index, len(self.solution) - 2, True)}" for index, value in enumerate(self.solution[1:])])}</p>")
        return lines

    def build_step_table(self, index):
        if len(self.steps) < index + 1:
            return
        return_arr = []
        step = self.steps[index]
        if index == 0:
            return_arr.append(f"<p>Initially Created Table:</p>")
        else:
            return_arr.append(f"<p>Step {index}:</p>")
        return_arr.append(f"<table>")
        return_arr.extend(self.create_table_top_row().split("\n"))
        return_arr.append(f"<tbody>")
        for a in step:
            return_arr.extend(self.create_table_row(a).split("\n"))
        return_arr.append(f"</tbody>")
        return_arr.append(f"</table>")
        return return_arr

    @staticmethod
    def create_table_row(row: []):
        return f"<tr>{"".join([f"<td>{ToHTMLConverter.value_format(a, True)}</td>" for a in row])}</tr>"

    def create_table_top_row(self):
        var_no = self.variable_no if self.problem_type == ProblemType.Maximization else self.constraints_no
        constraints_no = self.constraints_no if self.problem_type == ProblemType.Maximization else self.variable_no
        return (f"<thead>\n<tr>\n{"\n".join([f"<th>x<sub>{a}</sub></th>" for a in range(0, var_no)])}\n{"\n"
                .join([f"<th>y<sub>{a}</sub></th>" for a in range(0, constraints_no)])}"
                f"\n<th>Z</th>\n</tr>\n</thead>")

    def save_as_html(self, path: str):
        lines = ["<!DOCTYPE html>", "<html>", "<head>", "<meta charset='utf-8'>", "</head>", "<body>"]
        lines.extend(self.convert())
        lines.extend(["</body>", "</html>"])
        with open(path, "w", encoding='utf-8') as file:
            for line in lines:
                file.write(line)
