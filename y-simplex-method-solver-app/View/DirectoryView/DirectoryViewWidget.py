from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QPushButton
from .WorkingDirectoryView import WorkingDirectoryView


class DirectoryViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setLayout(self.vbox)
        self.up_directory_button = QPushButton("...Up", self)
        self.up_directory_button.setMinimumHeight(20)
        self.up_directory_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.working_directory_view = WorkingDirectoryView(self)
        self.up_directory_button.clicked.connect(self.working_directory_view.move_up_directory)
        self.vbox.addWidget(self.up_directory_button)
        self.vbox.addWidget(self.working_directory_view)
