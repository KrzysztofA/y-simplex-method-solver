from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
from Controller import SettingsController
from .SaveDirectoryField import SaveDirectoryField
from .SaveFileNameField import SaveFileNameField


class GeneralSettings(QWidget):
    def __init__(self, settings_controller: SettingsController):
        super().__init__()
        self.settings_controller = settings_controller
        self.vbox = QVBoxLayout()
        self.save_label = QLabel('Save Settings:')
        self.save_name_field = SaveFileNameField(settings_controller)
        self.save_dir_field = SaveDirectoryField(settings_controller)
        self.cache_last_dir_field = QCheckBox("Automatically Save in Last Directory: ")

        self.cache_last_dir_field.stateChanged.connect(self.set_cache_last_dir)

        self.setLayout(self.vbox)
        self.vbox.addWidget(self.save_label)
        self.vbox.addWidget(self.save_name_field)
        self.vbox.addWidget(self.save_dir_field)
        self.vbox.addWidget(self.cache_last_dir_field)

    def set_cache_last_dir(self):
        self.settings_controller.settings.use_last_save_dir = self.cache_last_dir_field.isChecked()

    def reset_setting(self):
        self.cache_last_dir_field.setChecked(self.settings_controller.settings.use_last_save_dir)
        self.save_name_field.reset_setting()
        self.save_dir_field.reset_setting()
