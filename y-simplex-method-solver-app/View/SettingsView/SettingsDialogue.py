from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QGridLayout, QDialogButtonBox, QStackedWidget
from Controller import SettingsController
from .GeneralSettings import GeneralSettings
from .SettingsMenu import SettingsMenu
from PyQt6.QtWidgets import QApplication
import os


class SettingsDialogue(QDialog):
    def __init__(self, settings_controller: SettingsController,  parent=None):
        super(SettingsDialogue, self).__init__(parent)

        self.settings_controller = settings_controller
        self.setWindowTitle("Settings")
        qbuttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Apply | QDialogButtonBox.StandardButton.Cancel
        self.setContentsMargins(0, 0, 0, 0)
        self.button_box = QDialogButtonBox(qbuttons)
        self.button_box.accepted.connect(self.accept_settings)
        self.button_box.rejected.connect(self.reject_settings)
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.reject_settings)

        self.grid_box = QGridLayout()
        self.setLayout(self.grid_box)

        self.settings_view = QStackedWidget()
        self.settings_menu = SettingsMenu(self.settings_view)
        self.general_settings = GeneralSettings(self.settings_controller)
        self.settings_view.addWidget(self.general_settings)

        self.grid_box.setVerticalSpacing(0)
        self.grid_box.setContentsMargins(0, 0, 0, 0)
        self.grid_box.addWidget(self.settings_menu, 0, 0)
        self.grid_box.addWidget(self.settings_view, 0, 1, 1, 3)
        self.grid_box.addWidget(self.button_box, 1, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)

    def accept_settings(self):
        self.settings_controller.save()
        self.accept()

    def reject_settings(self):
        self.settings_controller.load()
        self.general_settings.reset_setting()
        self.reject()

    def apply(self):
        self.settings_controller.save()

    def exec(self):
        self.general_settings.reset_setting()
        return super().exec()

    def open(self):
        self.general_settings.reset_setting()
        return super().open()
