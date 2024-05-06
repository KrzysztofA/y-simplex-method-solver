from Model import ProblemType, Singleton
import subprocess


class SimplexBackendController(metaclass=Singleton):
    def __init__(self):
        self.problem_type: ProblemType = ProblemType.Maximization
        self.collect_steps: bool = True
        self.values: [] = []

    def set_problem(self, problem):
        self.problem_type = problem

    def set_values(self, values: []):
        self.values = values

    def collect_values(self):
        if self.collect_steps:
            arg0 = "-maxsteps-ope" if self.problem_type == ProblemType.Maximization else "-minsteps-ope"
        else:
            arg0 = "-maxsol" if self.problem_type == ProblemType.Maximization else "-minsol"
        result = subprocess.run(["y-simplex-method-solver-executable.exe", arg0] + self.values, shell=True, capture_output=True, text=True)
        return result.stdout
