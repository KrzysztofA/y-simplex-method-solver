from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Settings:
    default_save_dir: str = "C://"
    use_last_save_dir: bool = False
    default_save_name: str = "New Simplex Solution"
    open_in_new_tab: bool = True

    compute_steps: bool = True
    include_computed_steps: bool = True
    add_graphs_to_exports: bool = False
    add_steps_to_exports: bool = False
    add_working_out_to_exports: bool = False
