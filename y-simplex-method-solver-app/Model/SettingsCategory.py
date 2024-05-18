from enum import Enum


class SettingsCategory(Enum):
    General = 0
    Editor = 1
    Export = 2
    Performance = 3

    @classmethod
    def string_list(cls):
        return ["General", "Editor", "Export", "Performance"]
