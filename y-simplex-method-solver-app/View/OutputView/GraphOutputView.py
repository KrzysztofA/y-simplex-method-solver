import math

from PyQt6.QtCore import Qt, QSize, QPointF
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QSizePolicy
import pyqtgraph as pg
from typing import List, Tuple


class GraphOutputView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_h_limits: int = 4

        self.results = []
        self.solution_ready = False

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        self.main_widget = QWidget(self)
        self.setWidget(self.main_widget)
        self.plot = pg.PlotWidget(self)
        self.plot.setMenuEnabled(False)
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
        self.checked_boxes_indexes: Tuple[int, int] = (0, 0)
        self.synchronize_variables(2)
        self.resizeEvent = self.on_resize
        self.solution_view = pg.ScatterPlotItem()
        self.solution_view.setPen(pg.mkPen(color=(100, 255, 100), width=5))
        self.solution_view.setData()
        self.plot.addItem(self.solution_view)
        self.function_line = pg.InfiniteLine(0, 0, movable=False, pen=pg.mkPen(color=(255, 100, 100), width=3))
        self.plot.addItem(self.function_line)
        self.constraint_lines = []
        self.plot.getPlotItem().getAxis('left').setWidth(40)
        self.plot.getPlotItem().getAxis('bottom').setHeight(40)

        self.constraint_functions = [[]]
        self.function_function = []

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
        self.plot.setMinimumHeight(int(event.size().height() * 3 / 5))
        if event.size().width() + self.verticalScrollBar().width() == event.oldSize().width():
            return
        self.change_grid_horizontal_limits(event.size().width() / 75)

    def synchronize_checked(self):
        if len(self.checked_boxes) == 2 and self.checked_boxes[1] not in self.variables:
            self.checked_boxes.remove(self.checked_boxes[1])
        if len(self.checked_boxes) >= 1 and self.checked_boxes[0] not in self.variables:
            self.checked_boxes.remove(self.checked_boxes[0])
        if len(self.checked_boxes) < 2:
            index = -1 if self.variables[-1] not in self.checked_boxes else -2
            self.variables[index].setChecked(True)
            self.checked_boxes.append(self.variables[index])
            self.synchronize_checked()
        if len(self.checked_boxes) == 2:
            self.checked_boxes_indexes = (
                self.variables.index(self.checked_boxes[0]), self.variables.index(self.checked_boxes[1]))
            self.set_labels()

    def on_check(self, box: QCheckBox):
        if box.checkState() == Qt.CheckState.Unchecked and box in self.checked_boxes:
            box.setChecked(True)
        elif box not in self.checked_boxes and len(self.checked_boxes) >= 2:
            temp = self.checked_boxes[0]
            self.checked_boxes.pop(0)
            temp.setChecked(False)
            self.checked_boxes.append(box)
        if len(self.checked_boxes) >= 2:
            self.checked_boxes_indexes = (
                self.variables.index(self.checked_boxes[0]), self.variables.index(self.checked_boxes[1]))
            self.set_labels()
            self.set_constraints_values()
        self.display_selected_variables()

    def set_labels(self):
        self.plot.getPlotItem().setLabel('bottom', self.checked_boxes[0].text())
        self.plot.getPlotItem().setLabel('left', self.checked_boxes[1].text())

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

    def set_result(self, result: []):
        self.results = [float(a.split("/")[0]) / float(a.split("/")[1]) if "/" in a else float(a) for a in result]
        print(self.results)
        self.solution_ready = True
        self.display_selected_variables()

    def on_constraint_change(self):
        self.solution_ready = False
        self.solution_view.setData()

    def on_function_change(self):
        self.solution_ready = False
        self.solution_view.setData()

    def display_selected_variables(self):
        if self.solution_ready:
            point = (self.results[self.checked_boxes_indexes[0] + 1], self.results[self.checked_boxes_indexes[1] + 1])
            self.solution_view.setData([point[0]], [point[1]])

    def set_function(self, function):
        angle = self.get_angle(function)
        self.function_line.setPos(self.get_point(function))
        self.function_line.setAngle(angle)

    def update_constraint_functions(self, functions):
        self.constraint_functions = functions
        if len(self.constraint_functions) < len(self.constraint_lines):
            for i in range(len(self.constraint_functions), len(self.constraint_lines)):
                self.plot.removeItem(self.constraint_lines[i])

        elif len(self.constraint_functions) > len(self.constraint_lines):
            for i in range(len(self.constraint_lines), len(self.constraint_functions)):
                angle = self.get_angle(self.constraint_functions[i])
                self.constraint_lines.append(pg.InfiniteLine(self.get_point(self.constraint_functions[i]), angle))
                self.plot.addItem(self.constraint_lines[-1])
        self.set_constraints_values()

    def set_constraints_values(self):
        for i in range(len(self.constraint_lines)):
            self.set_constraint_values(i, self.constraint_functions[i])

    def set_constraint_values(self, index, function):
        angle = self.get_angle(function)
        self.constraint_lines[index].setPos(self.get_point(function))
        self.constraint_lines[index].setAngle(angle)

    def get_point(self, function):
        y_coefficient = function[self.checked_boxes_indexes[1] + 1]
        x_coefficient = function[self.checked_boxes_indexes[0] + 1]
        x_part = 0
        y_part = 0
        if x_coefficient != 0:
            x_part = function[0] / x_coefficient
        elif y_coefficient != 0:
            y_part = function[0] / y_coefficient

        return QPointF(x_part, y_part)

    def get_angle(self, function):
        from_point = self.get_point(function)
        if function[self.checked_boxes_indexes[0]] == 0:
            angle = 0
        elif function[self.checked_boxes_indexes[1]] == 0:
            angle = 90
        else:
            angle = math.degrees(math.atan2(function[self.checked_boxes_indexes[1] + 1] / function[0], function[self.checked_boxes_indexes[0] + 1] / function[0]))
        return angle
