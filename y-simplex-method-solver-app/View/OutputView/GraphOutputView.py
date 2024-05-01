from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QSizePolicy
import pyqtgraph as pg
from typing import List


class GraphOutputView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_h_limits: int = 4

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        self.main_widget = QWidget(self)
        self.setWidget(self.main_widget)
        self.plot = pg.PlotWidget(self)
        self.plot.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.vbox = QVBoxLayout()
        self.main_widget.setLayout(self.vbox)
        self.vbox.addWidget(self.plot)
        self.plot.setTitle('Visualization')
        self.label = QLabel(parent=self, text="Select 2 variables to plot:")
        self.vbox.addWidget(self.label)
        self.variables_box = QWidget(self)
        self.variables_box_layout = QVBoxLayout()
        self.variables_box.setLayout(self.variables_box_layout)
        self.vbox.addWidget(self.variables_box)
        self.variables: List[QCheckBox] = []
        self.checked_boxes: List[QCheckBox] = []
        self.synchronize_variables(2)
        self.resizeEvent = self.on_resize

    def synchronize_variables(self, var_no: int):
        if var_no < len(self.variables):
            for i in self.variables[var_no:]:
                self.remove_from_grid(i)
                self.variables.remove(i)
        else:
            old_len = len(self.variables)
            for i in range(len(self.variables), var_no):
                temp = QCheckBox(f'x{i}')
                self.variables.append(temp)
                func = lambda x, a=i: self.on_check(self.variables[a])
                self.variables[-1].toggled.connect(func)
            for i in range(old_len, len(self.variables)):
                self.add_to_grid(self.variables[i])
        self.synchronize_checked()

    def on_resize(self, event: QResizeEvent):
        self.parent().resizeEvent(event)
        self.plot.setMinimumWidth(event.size().width())
        self.plot.setMinimumHeight(int(event.size().height()*3/5))
        if event.size().width() + self.verticalScrollBar().width() == event.oldSize().width():
            return
        self.change_grid_horizontal_limits(event.size().width() / 75)
        """
        if event.size().width() > 275 >= event.oldSize().width():
            self.change_grid_horizontal_limits(5)
        elif event.size().width() > 225 >= event.oldSize().width() or event.size().width() < 275 <= event.oldSize().width():
            self.change_grid_horizontal_limits(4)
        elif event.size().width() > 190 >= event.oldSize().width() or event.size().width() < 215 <= event.oldSize().width():
            self.change_grid_horizontal_limits(3)
        elif event.size().width() < 190 <= event.oldSize().width():
            self.change_grid_horizontal_limits(2)
        """

    def synchronize_checked(self):
        if len(self.checked_boxes) < 2:
            index = -2 if self.variables[-2] not in self.checked_boxes else -1
            self.variables[index].setChecked(True)
            self.checked_boxes.append(self.variables[index])
            self.synchronize_checked()

    def on_check(self, box: QCheckBox):
        if box.checkState() == Qt.CheckState.Unchecked and box in self.checked_boxes:
            box.setChecked(True)
        elif box not in self.checked_boxes and len(self.checked_boxes) >= 2:
            temp = self.checked_boxes[0]
            self.checked_boxes.pop(0)
            temp.setChecked(False)
            self.checked_boxes.append(box)

    def change_grid_horizontal_limits(self, new_limits: int):
        if new_limits != self.grid_h_limits:
            self.grid_h_limits = new_limits
            self.restructure_grid()

    def add_to_grid(self, widget: QWidget):
        if self.variables_box_layout.count() == 0:
            temp_widget = QWidget()
            temp = QHBoxLayout(temp_widget)
            temp_widget.setLayout(temp)
            temp.addWidget(widget)
            self.variables_box_layout.addWidget(temp_widget)
        else:
            last_layout = self.variables_box_layout.itemAt(self.variables_box_layout.count() - 1).widget().layout()
            if last_layout.count() >= self.grid_h_limits:
                temp = QHBoxLayout()
                temp_widget = QWidget()
                temp_widget.setLayout(temp)
                self.variables_box_layout.addWidget(temp_widget)
                temp.addWidget(widget)
            else:
                last_layout.addWidget(widget)

    def remove_from_grid(self, widget: QWidget):
        for i in range(self.variables_box_layout.count() - 1, -1, -1):
            item = self.variables_box_layout.itemAt(i).widget().layout()
            for j in range(item.count() - 1, -1, -1):
                item2 = item.itemAt(j)
                if widget == item2.widget():
                    item.removeItem(item2)
        self.restructure_grid()

    def restructure_grid(self):
        temp_arr = []
        for i in range(self.variables_box_layout.count() - 1, -1, -1):
            item = self.variables_box_layout.itemAt(i).widget()
            for j in range(item.layout().count() - 1, -1, -1):
                item2 = item.layout().itemAt(j)
                temp_arr.append(item2.widget())
                item.layout().removeItem(item2)
            self.variables_box_layout.removeWidget(item)
            item.deleteLater()
        for i in reversed(temp_arr):
            self.add_to_grid(i)
