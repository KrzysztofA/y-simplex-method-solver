from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Dict
from Model import ProblemType, ResultStruct


@dataclass_json
@dataclass
class FullSolutionStruct:
    function: str
    constraints: Dict[int, str]
    result: ResultStruct
    problem: ProblemType = ProblemType.Maximization
    variable_no: int = 0
    constraint_no: int = 0
