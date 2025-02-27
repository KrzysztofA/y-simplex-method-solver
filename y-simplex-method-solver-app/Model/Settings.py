from dataclasses import dataclass
from enum import auto
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Settings:
    # General - Save
    default_save_dir: str = "C://"
    use_last_save_dir: bool = False
    default_save_name: str = "New Simplex Solution"
    open_in_new_tab: bool = True
    
    # Editor
    font_size: int = 8
    default_theme: str = "OS Setting"
    
    # Export
    add_graphs_to_exports: bool = False
    add_steps_to_exports: bool = False

    # Performance
    compute_steps: bool = True
    auto_refresh_graphs: bool = False
    add_working_out_to_exports: bool = False

    include_computed_steps: bool = True
