import os

from Model import Settings
from os import path
import pathlib
from Model import Singleton
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

class SettingsController(metaclass=Singleton):
    """
    This class is responsible for managing the settings of the application.
    It is a singleton class, so only one instance of it can exist at a time.
    It stores the settings in a JSON file, and can load and save them, as well as apply them to the application.
    """
    def __init__(self):
        self.settings_directory = path.join("Files", "Other")
        self.settings = Settings()
        self.load()
        self.save()
        self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)

    def change_font_size(self, font_size: int):
        """
        Changes the font size of the application.
        """
        self.settings.font_size = font_size
    
    def change_font_style(self, font_style: str):
        """
        Changes the font style of the application.
        """
        self.settings.font_style = font_style
        
    def save(self):
        """
        Saves the settings to a JSON file and applies the settings which require application.
        """
        # Save the JSON file with settings        
        json_file = self.settings.to_json()
        if not path.isdir(self.settings_directory):
            os.mkdir("Files")
            os.mkdir(self.settings_directory)
        with open(path.join(self.settings_directory, "settings.json"), "w") as settings_file:
            settings_file.write(json_file)
        self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)
        
        # Apply the settings which require applying
        self.apply_font_settings()

    def load(self) -> bool:
        """
        Loads the settings from a JSON file.
        """
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
        """
        Automatically sets the default save path to the directory of the last saved file.
        """
        if self.settings.use_last_save_dir:
            path_obj = pathlib.Path(new_path)
            if path_obj.is_dir():
                self.settings.default_save_dir = str(path_obj)
                self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)
            else:
                self.settings.default_save_dir = str(path_obj.parent)
                self.default_save_path = path.join(self.settings.default_save_dir, self.settings.default_save_name)

    def apply_font_settings(self):
        """
        Applies the font settings to the application.
        """
        temp_font = QFont(self.settings.font_style, self.settings.font_size)
        QApplication.instance().setFont(temp_font)