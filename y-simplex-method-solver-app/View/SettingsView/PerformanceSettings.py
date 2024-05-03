from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel
from Controller import SettingsController


class PerformanceSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor_performance_settings_label = QLabel("Editor Performance Settings:")
        self.include_graphs_to_export = QCheckBox("Graphs")
        self.include_graphs_to_export.setChecked(False)
        self.simplex_method_settings_include = QLabel("Include Computing of the Following Data")
        self.auto_refresh_graph = QCheckBox("Auto-Refresh Graphs on any change")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.editor_performance_settings_label)
        self.vbox.addWidget(self.include_graphs_to_export)
        self.setLayout(self.vbox)
