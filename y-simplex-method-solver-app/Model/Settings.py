from dataclasses import dataclass


@dataclass
class Settings:
    compute_steps: bool = False
    default_save_dir = "C://"
    default_save_name = "New Simplex Solution"

