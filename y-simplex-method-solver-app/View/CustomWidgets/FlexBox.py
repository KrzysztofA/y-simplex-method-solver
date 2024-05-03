from functools import reduce

from PyQt6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt
from enum import Enum
from typing import List, Callable


class Direction(Enum):
    Row = 1,
    Column = 2


class FlexBox(QScrollArea):
    def __init__(self, direction: Direction = Direction.Row, parent: QWidget | None = None, gap: int = 5, deduce_element_size: bool = False, element_size: int = 75, deduce_limits: bool = False, limits: int = 2):
        super().__init__(parent)
        self.direction = direction
        self.main_layout: QHBoxLayout | QVBoxLayout = QVBoxLayout(self) if self.direction == Direction.Row else QHBoxLayout(self)
        self.gap = gap
        if direction == Direction.Row:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if direction == Direction.Column:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.automatically_deduce_limits = deduce_limits
        self.deduce_element_size = deduce_element_size
        self.element_size = element_size
        self.elements_included_in_calculation = [self.verticalScrollBar() if direction == Direction.Row else self.horizontalScrollBar()]
        self.on_resize_pre_events = []
        self.on_resize_post_events = []
        self.widgets: List[QWidget] = []
        self.limits = self.deduce_limits(parent.size().width() if self.direction == Direction.Row else parent.size().height() ) if self.automatically_deduce_limits else self.limits = limits

    def deduce_limits(self, available_size: int):
        max_size = 0
        if self.deduce_element_size and self.direction == Direction.Row:
            for widget in self.widgets:
                max_size = max_size if max_size > widget.width() + self.gap else widget.width() + self.gap
        elif self.deduce_element_size and self.direction == Direction.Column:
            for widget in self.widgets:
                max_size = max_size if max_size > widget.height() + self.gap else widget.height() + self.gap
        else:
            max_size = self.element_size
        return int(available_size / max_size)

    def on_resize(self, event: QResizeEvent):
        self.parent().resizeEvent(event)
        for pre_event in self.on_resize_pre_events:
            pre_event()
        if self.direction == Direction.Column and event.size().height() + reduce(lambda x, y: x + y.height(), self.elements_included_in_calculation, 0) == event.oldSize().height() \
            or self.direction == Direction.Row and event.size().width() + reduce(lambda x, y: x + y.width(), self.elements_included_in_calculation, 0) == event.oldSize().width():
            return
        if self.automatically_deduce_limits:
            self.limits = self.deduce_limits(event.size().width() if self.direction == Direction.Row else event.size().height())
            self.restructure()
        for post_event in self.on_resize_post_events:
            post_event()

    def change_limits(self, new_limits: int):
        self.automatically_deduce_limits = False
        if new_limits != self.limits:
            self.limits = new_limits
            self.restructure()

    def add_widget(self, widget: QWidget):
        if self.main_layout.count() == 0:
            temp_widget = QWidget()
            temp = QHBoxLayout(temp_widget) if self.direction == Direction.Row else QVBoxLayout(temp_widget)
            temp.setSpacing(self.gap)
            temp_widget.setLayout(temp)
            temp.addWidget(widget)
            self.main_layout.addWidget(temp_widget)
        else:
            last_layout = self.main_layout.itemAt(self.main_layout.count() - 1).widget().layout()
            if last_layout.count() >= self.limits:
                temp = QHBoxLayout() if self.direction == Direction.Row else QVBoxLayout()
                temp.setSpacing(self.gap)
                temp_widget = QWidget()
                temp_widget.setLayout(temp)
                self.main_layout.addWidget(temp_widget)
                temp.addWidget(widget)
            else:
                last_layout.addWidget(widget)

    def remove_widget(self, widget: QWidget):
        for i in range(self.main_layout.count() - 1, -1, -1):
            item = self.main_layout.itemAt(i).widget().layout()
            for j in range(item.count() - 1, -1, -1):
                item2 = item.itemAt(j)
                if widget == item2.widget():
                    item.removeItem(item2)
        self.restructure()

    def restructure(self):
        temp_arr = []
        for i in range(self.main_layout.count() - 1, -1, -1):
            item = self.main_layout.itemAt(i).widget()
            for j in range(item.layout().count() - 1, -1, -1):
                item2 = item.layout().itemAt(j)
                temp_arr.append(item2.widget())
                item.layout().removeItem(item2)
            self.main_layout.removeWidget(item)
            item.deleteLater()
        for i in reversed(temp_arr):
            self.add_widget(i)
