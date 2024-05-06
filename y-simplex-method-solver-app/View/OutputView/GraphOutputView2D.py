from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from View.CustomWidgets import FlexBox
import pyqtgraph as pg


class GraphOutputView2D(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.variables_box = FlexBox(parent=self, use_scroll_bar=False)
        self.vbox = QVBoxLayout()
        self.plot = pg.plot()
        self.vbox.addWidget(self.plot)
        self.vbox.addWidget(self.variables_box)
