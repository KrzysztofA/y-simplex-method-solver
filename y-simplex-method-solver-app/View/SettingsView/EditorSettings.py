from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout, QComboBox, QApplication
from Controller import SettingsController


class EditorSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.include_label = QLabel("General")
        self.font_size_widget = QWidget(self)
        self.font_size_layout = QHBoxLayout()
        self.font_size_label = QLabel("Font Size: ", self.font_size_widget)
        self.font_size = QSpinBox(self.font_size_widget)
        self.font_size_layout.addWidget(self.font_size_label)
        self.font_size_layout.addWidget(self.font_size)
        self.font_size_widget.setLayout(self.font_size_layout)
        self.use_default_theme = QCheckBox("Use Default Theme")

        self.default_theme_combo_box = QComboBox(self)
        self.default_theme_combo_box.addItem("OS Setting")
        self.default_theme_combo_box.setCurrentText("OS Setting")
        self.default_theme_combo_box.addItem("Light")
        self.default_theme_combo_box.addItem("Dark")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.include_label)
        self.vbox.addWidget(self.font_size_widget)
        self.vbox.addWidget(self.use_default_theme)
        self.vbox.addWidget(self.default_theme_combo_box)
        self.setLayout(self.vbox)
