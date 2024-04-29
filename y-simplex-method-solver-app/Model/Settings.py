from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Settings:
    compute_steps: bool = True
    default_save_dir: str = "C://"
    use_last_save_dir: bool = False
    default_save_name: str = "New Simplex Solution"
    open_in_new_tab: bool = True
