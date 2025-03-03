from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel
from Controller import SettingsController


class PerformanceSettings(QWidget):
    """
    PerformanceSettings class is a QWidget that contains the settings for the performance options of the editor.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor_performance_settings_label = QLabel("Editor Performance Settings:")
        self.simplex_method_settings_include = QLabel("Include Computing of the Following Data")
        self.auto_refresh_graph = QCheckBox("Auto-Refresh Graphs on any change")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.editor_performance_settings_label)
        self.vbox.addWidget(self.simplex_method_settings_include)
        self.vbox.addWidget(self.auto_refresh_graph)
        self.setLayout(self.vbox)

    def reset_setting(self):
        """
        Resets all settings to the last saved settings.
        """
        self.auto_refresh_graph.setChecked(SettingsController().settings.auto_refresh_graphs)
        