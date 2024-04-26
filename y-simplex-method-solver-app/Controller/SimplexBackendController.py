from Model import ProblemType
import subprocess


class SimplexBackendController:
    def __init__(self):
        self.problem_type: ProblemType = ProblemType.Maximization
        self.values: [] = []

    def set_problem(self, problem):
        self.problem_type = problem

    def set_values(self, values: []):
        self.values = values

    def collect_values(self):
        arg0 = "-maxsol" if self.problem_type == ProblemType.Maximization else "-minsol"
        result = subprocess.run(["./y-simplex-method-solver-executable", arg0] + self.values, capture_output=True, text=True)
        return result.stdout
