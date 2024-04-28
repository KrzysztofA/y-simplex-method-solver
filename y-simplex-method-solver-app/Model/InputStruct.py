from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
from Model import ProblemType


@dataclass_json
@dataclass
class InputStruct:
    function_input: List[str]
    constraints: List[List[str]]
    problem: ProblemType
    variable_no: int
    constraint_no: int
