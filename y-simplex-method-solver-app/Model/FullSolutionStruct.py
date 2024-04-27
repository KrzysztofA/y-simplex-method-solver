from dataclasses import dataclass
from Model import *


@dataclass
class FullSolutionStruct:
    function: []
    constraints: []
    result: ResultStruct
    problem: ProblemType = ProblemType.Maximization
    variable_no: int = 0
    constraint_no: int = 0
