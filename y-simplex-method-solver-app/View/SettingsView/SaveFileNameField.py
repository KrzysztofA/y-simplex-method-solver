from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QApplication, QLabel
from Controller import SettingsController


class SaveFileNameField(QWidget):
    def __init__(self, settings_controller: SettingsController):
        super().__init__()
        self.settings_controller = settings_controller
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)

        self.save_filename_line_edit_settings = QLineEdit(self)
        self.save_filename_line_edit_settings.setText(self.settings_controller.settings.default_save_name)
        QApplication.instance().focusChanged.connect(self.unfocus_line_edit)

        self.hbox.addWidget(QLabel('Default name: '))
        self.hbox.addWidget(self.save_filename_line_edit_settings)

    def reset_setting(self):
        self.save_filename_line_edit_settings.setText(self.settings_controller.settings.default_save_name)

    def unfocus_line_edit(self, old_widget: QWidget, new_widget: QWidget):
        if old_widget == self.save_filename_line_edit_settings:
            new_name = self.save_filename_line_edit_settings.text()
            self.change_save_file_name(new_name)

    def change_save_file_name(self, new_name: str):
        self.save_filename_line_edit_settings.setText(new_name)
        self.settings_controller.settings.default_save_name = new_name
