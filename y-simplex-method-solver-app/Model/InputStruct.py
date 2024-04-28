from dataclasses import dataclass
from dataclasses_json import dataclass_json
from Model import ProblemType
from typing import Dict


@dataclass_json
@dataclass
class InputStruct:
    function_input: str
    constraints: Dict[int, str]
    problem: ProblemType
    variable_no: int
    constraint_no: int
