from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .InputStruct import InputStruct
from .FullSolutionStruct import FullSolutionStruct


@dataclass_json
@dataclass
class SimplexFile:
    filename: str
    input: InputStruct
    output: FullSolutionStruct
