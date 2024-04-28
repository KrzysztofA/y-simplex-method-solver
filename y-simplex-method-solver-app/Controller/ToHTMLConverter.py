from typing import List
import re

from Model import ProblemType


class ToHTMLConverter:
    def __init__(self):
        self.problem_type: ProblemType = ProblemType.Maximization
        self.equation: List[str] = []
        self.constraints: List[str] = []
        self.solution: List[str] = []

        # Steps only vars
        self.steps: List[str] = []
        self.operations: List[str] = []
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

    def set_operations(self, operations: List[str]):
        self.operations = operations

    def set_variable_no(self, variable_no: int):
        self.variable_no = variable_no

    def set_constraints_no(self, constraints_no: int):
        self.constraints_no = constraints_no

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
        function_delim = "&#x2264;" if self.problem_type == ProblemType.Maximization else "&#8805;"
        lines.append(
            f"<p>{"Maximize" if self.problem_type == ProblemType.Maximization else "Minimize"} the following equation:</p>")
        lines.append(
            f"<p>Z {function_delim} {"".join([f"{self.value_format(value)}{self.variable_format(value, index)}{self.all_but_last_format(" + ", value, index, len(self.equation) - 2)}" for index, value in enumerate(self.equation[:-1])])}</p>")
        lines.append("<p>Subject to constraints:</p>")
        lines.append("<p>")
        for i in self.constraints:
            i_arr = [a.strip() for a in i.split(",")]
            lines.append(
                f"<div>{"".join([f"{self.value_format(value)}{self.variable_format(value, index)}{self.all_but_last_format(" + ", value, index, len(i_arr) - 2)}" for index, value in enumerate(i_arr[:-1])])} {function_delim} {self.value_format(i_arr[-1], True)}</div>")
        lines.append("</p>")
        if len(self.steps) != 0:
            for i in range(0, len(self.steps)):
                if 0 < i:
                    lines.append(f"<p><div><b>Step {i}:</b></div></p>")
                    lines.append(f"<p>")
                    lines.extend(self.build_operations_text(i))
                    lines.append("</p>")
                lines.extend(self.build_step_table(i))
        if len(self.solution) != 0:
            lines.append("<p>After the computation, the following results were obtained:</p>")
            lines.append(
                f"<p>Z = {self.value_format(self.solution[0], True)}, {" ".join([f"x<sub>{index}</sub> = {self.value_format(value, True)}{self.all_but_last_format(",", value, index, len(self.solution) - 2, True)}" for index, value in enumerate(self.solution[1:])])}</p>")
        return lines

    def build_operations_text(self, index):
        if len(self.steps) < index:
            return
        return_arr = []
        operation = self.operations[index - 1]
        for i in operation[1:]:
            if "(" in i:
                b = [a for a in re.split("\(|\)", i)]
                i = f"{b[0]} {self.value_format(b[1], True)}"
                i = i.replace("/ ", " &#247; ")
            else:
                var = re.search("\s(-\d+|\d+)([/\d]+)", i)
                if var is not None:
                    out = self.value_format(var.group(), True)
                    i = re.sub("\s(-\d+|\d+)([/\d]+)", f" {out} ", i)
            matches = list(re.finditer('Row[\d]+', i))
            for match in reversed(matches):
                i = i[:match.end()] + "</sub>" + i[match.end():]
            return_arr.append(f"<div>{i.replace("Row", "Row<sub>")}</div>")
        return return_arr

    def build_step_table(self, index):
        if len(self.steps) < index + 1:
            return
        return_arr = []
        step = self.steps[index]
        if index == 0:
            return_arr.append(f"<p>Initially Created Table:</p>")
        elif index == len(self.steps) - 1:
            return_arr.append(f"<p>Lead to creation of the following, final table:</p>")
        else:
            return_arr.append(f"<p>Lead to creation of the following table:</p>")
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
        variable = "x" if self.problem_type == ProblemType.Maximization else "y"
        slack = "y" if self.problem_type == ProblemType.Maximization else "s"
        z = self.problem_type == ProblemType.Maximization
        constraints_no = self.constraints_no if self.problem_type == ProblemType.Maximization else self.variable_no
        return (f"<thead>\n<tr>\n{"\n".join([f"<th>{variable}<sub>{a}</sub></th>" for a in range(0, var_no)])}\n{"\n"
                .join([f"<th>{slack}<sub>{a}</sub></th>" for a in range(0, constraints_no)])}"
                f"{f"\n<th>Z</th>\n" if z else ""}</tr>\n</thead>")

    def save_as_html(self, path: str):
        lines = ["<!DOCTYPE html>", "<html>", "<head>", "<meta charset='utf-8'>", "</head>", "<body>"]
        lines.extend(self.convert())
        lines.extend(["</body>", "</html>"])
        with open(path, "w", encoding='utf-8') as file:
            for line in lines:
                file.write(line)
