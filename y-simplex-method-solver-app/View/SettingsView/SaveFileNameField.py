from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QApplication, QLabel
from Controller import SettingsController


class SaveFileNameField(QWidget):
    """
    A widget that allows the user to change the default name of the save file.
    """
    def __init__(self):
        super().__init__()
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)

        self.save_filename_line_edit_settings = QLineEdit(self)
        self.save_filename_line_edit_settings.setText(SettingsController().settings.default_save_name)
        QApplication.instance().focusChanged.connect(self.unfocus_line_edit)

        self.hbox.addWidget(QLabel('Default name: '))
        self.hbox.addWidget(self.save_filename_line_edit_settings)

    def reset_setting(self):
        """
        Resets the settings to the last saved value.
        """
        self.save_filename_line_edit_settings.setText(SettingsController().settings.default_save_name)

    def unfocus_line_edit(self, old_widget: QWidget, new_widget: QWidget):
        """
        On unfocus, save the new name.
        """
        if old_widget == self.save_filename_line_edit_settings:
            new_name = self.save_filename_line_edit_settings.text()
            self.change_save_file_name(new_name)

    def change_save_file_name(self, new_name: str):
        """
        Changes the default name of the save file.
        """
        self.save_filename_line_edit_settings.setText(new_name)
        SettingsController().settings.default_save_name = new_name
