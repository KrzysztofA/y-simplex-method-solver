from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel
from Controller import SettingsController


class ExportSettings(QWidget):
    """
    Export settings contains the settings for the exporting of data. It decides what data to include in the exports.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.include_label = QLabel("Include following data:")
        self.include_graphs_to_export = QCheckBox("Graphs")
        self.include_graphs_to_export.setChecked(False)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.include_label)
        self.vbox.addWidget(self.include_graphs_to_export)
        self.setLayout(self.vbox)

    def reset_setting(self):
        self.include_graphs_to_export.setChecked(SettingsController().settings.add_graphs_to_exports)
        