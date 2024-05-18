from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Dict


@dataclass_json
@dataclass
class ResultStruct:
    solution: str
    steps: Dict[int, str]
    operations: Dict[int, str]
