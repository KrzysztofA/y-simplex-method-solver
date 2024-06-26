import os

from Model import Settings
from os import path
import pathlib
from cryptography.fernet import Fernet
from Model import Singleton


class SettingsController(metaclass=Singleton):
    def __init__(self):
        self.settings_directory = path.join("Files", "Other")
        self.settings = Settings()
        self.load()
        self.save()
        self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)

    def save(self):
        json_file = self.settings.to_json()
        if not path.isdir(self.settings_directory):
            os.mkdir("Files")
            os.mkdir(self.settings_directory)
        with open(path.join(self.settings_directory, "settings.json"), "w") as settings_file:
            settings_file.write(json_file)
        self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)

    def load(self) -> bool:
        json_path = path.join(self.settings_directory, "settings.json")
        if not os.access(json_path, os.R_OK):
            return False
        try:
            with open(path.join(self.settings_directory, "settings.json"), "r") as settings_file:
                settings_data = settings_file.read()
                self.settings = Settings.from_json(settings_data)
        except FileNotFoundError:
            return False
        self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)
        return True

    def auto_set_default_save_path(self, new_path: str):
        if self.settings.use_last_save_dir:
            path_obj = pathlib.Path(new_path)
            if path_obj.is_dir():
                self.settings.default_save_dir = str(path_obj)
                self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)
            else:
                self.settings.default_save_dir = str(path_obj.parent)
                self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)
