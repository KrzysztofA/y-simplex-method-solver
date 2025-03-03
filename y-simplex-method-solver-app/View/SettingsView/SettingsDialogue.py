from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QGridLayout, QDialogButtonBox, QStackedWidget
from Controller import SettingsController
from .ExportSettings import ExportSettings
from .GeneralSettings import GeneralSettings
from .SettingsMenu import SettingsMenu
from .EditorSettings import EditorSettings
from .PerformanceSettings import PerformanceSettings
from PyQt6.QtWidgets import QApplication
import os


class SettingsDialogue(QDialog):
    """
    The settings dialogue is a dialog that allows the user to change the settings of the application.
    The settings are saved when the user clicks on the "Ok" button, and are loaded when the user clicks on the "Cancel" button.
    The settings are applied when the user clicks on the "Apply" button.
    The dialogue consists of all the QWidgets that are used to change the settings.
    """
    def __init__(self, parent=None):
        super(SettingsDialogue, self).__init__(parent)
        self.setWindowTitle("Settings")
        
        # Set the QButtons to be displayed at the bottom of the SettingsDialogue
        qbuttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Apply | QDialogButtonBox.StandardButton.Cancel
        self.setContentsMargins(0, 0, 0, 0)
        self.button_box = QDialogButtonBox(qbuttons)
        self.button_box.accepted.connect(self.accept_settings)
        self.button_box.rejected.connect(self.reject_settings)
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.reject_settings)

        self.grid_box = QGridLayout()
        self.setLayout(self.grid_box)

        # Create and add all the settings widgets
        self.settings_view = QStackedWidget()
        self.settings_menu = SettingsMenu(self.settings_view)
        self.general_settings = GeneralSettings()
        self.editor_settings = EditorSettings()
        self.export_settings = ExportSettings()
        self.performance_settings = PerformanceSettings()
        self.settings_view.addWidget(self.general_settings)
        self.settings_view.addWidget(self.editor_settings)
        self.settings_view.addWidget(self.export_settings)
        self.settings_view.addWidget(self.performance_settings)
        self.settings_menu.to_change = self.settings_view
        
        # Set the layout of the SettingsDialogue
        self.grid_box.setVerticalSpacing(0)
        self.grid_box.setContentsMargins(0, 0, 0, 0)
        self.grid_box.addWidget(self.settings_menu, 0, 0)
        self.grid_box.addWidget(self.settings_view, 0, 1, 1, 3)
        self.grid_box.addWidget(self.button_box, 1, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)

    def accept_settings(self):
        """
        On accept, save the settings
        """
        SettingsController().save()
        self.accept()

    def reject_settings(self):
        """
        On reject, load the former settings
        """
        SettingsController().load()
        self.reset_settings()
        self.reject()

    def apply(self):
        """
        On apply, save the settings
        """
        SettingsController().save()

    def exec(self):
        """
        When dialog is closed, reset the settings
        """
        self.reset_settings()
        return super().exec()

    def open(self):
        """
        When the dialog is opened, the settings are reset to the last saved settings.
        """
        self.reset_settings()
        return super().open()

    def reset_settings(self):
        """
        Reset the settings to the last saved settings.
        """
        self.general_settings.reset_setting()
        self.editor_settings.reset_setting()
        self.export_settings.reset_setting()
        self.performance_settings.reset_setting()