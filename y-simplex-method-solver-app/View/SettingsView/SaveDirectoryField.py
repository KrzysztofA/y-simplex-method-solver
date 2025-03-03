from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QApplication
from Controller import SettingsController
import os


class SaveDirectoryField(QWidget):
    """
    Widget responsible for changing the default save directory.
    """
    def __init__(self):
        super().__init__()
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)

        self.save_directory_line_edit_settings = QLineEdit(self)
        self.save_directory_line_edit_settings.setText(SettingsController().settings.default_save_dir)
        QApplication.instance().focusChanged.connect(self.unfocus_line_edit)

        self.save_directory_select_button = QPushButton("Select Directory")
        self.save_directory_select_button.clicked.connect(self.choose_save_directory)

        self.hbox.addWidget(self.save_directory_line_edit_settings)
        self.hbox.addWidget(self.save_directory_select_button)

    def reset_setting(self):
        """
        Resets the settings to the last saved value.
        """
        self.save_directory_line_edit_settings.setText(SettingsController().settings.default_save_dir)

    def unfocus_line_edit(self, old_widget: QWidget, new_widget: QWidget):
        """
        On unfocus, save the new directory.
        """
        if old_widget == self.save_directory_line_edit_settings:
            try_path = self.save_directory_line_edit_settings.text()
            if os.path.isdir(try_path):
                self.change_save_directory(try_path)

    def choose_save_directory(self):
        """
        Opens a file dialog to choose a new save directory.
        """
        new_directory = QFileDialog.getExistingDirectory(self, "Select Directory", directory=SettingsController().settings.default_save_dir)
        if new_directory:
            self.change_save_directory(new_directory)

    def change_save_directory(self, path: str):
        """
        Changes the default save directory.
        """
        if os.path.isdir(path):
            self.save_directory_line_edit_settings.setText(path)
            SettingsController().settings.default_save_dir = path
