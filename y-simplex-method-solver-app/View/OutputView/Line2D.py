from pyqtgraph import InfiniteLine
from PyQt6.QtCore import QPointF
import math
from typing import Tuple
from Model import ProblemType


class Line2D(InfiniteLine):
    def __init__(self, function, index_x, index_y):
        self.function = function
        self.index_x = index_x
        self.index_y = index_y
        self.intersect_x, self.intersect_y = self.calculate_axes_intersections()

        # In form (a, b) where ax + b = y
        self.equation = self.calculate_equation()
        self.angle = self.calculate_angle()
        super().__init__(pos=self.intersect_x, angle=self.angle)

    def calculate_angle(self):
        return math.degrees(math.atan2(self.intersect_x.y() - self.intersect_y.y(), self.intersect_x.x() - self.intersect_y.x()))

    def set_function(self, function):
        if self.function == function:
            return
        self.function = function
        self.recalculate_line()

    def set_index_x(self, index_x):
        if self.index_x == index_x:
            return
        self.index_x = index_x
        self.recalculate_line()

    def set_index_y(self, index_y):
        if self.index_y == index_y:
            return
        self.index_y = index_y
        self.recalculate_line()

    def check_point(self, point: QPointF, problem: ProblemType) -> bool:
        if problem == ProblemType.Maximization:
            return self.check_point_below(point)
        elif problem == ProblemType.Minimization:
            return self.check_point_above(point)

    def check_point_below(self, point: QPointF):
        true_y = self.equation[0] * point.x() + self.equation[1]
        return true_y >= point.y() or math.isclose(true_y, point.y())

    def check_point_above(self, point: QPointF):
        true_y = self.equation[0] * point.x() + self.equation[1]
        return true_y <= point.y() or math.isclose(true_y, point.y())

    def recalculate_line(self):
        self.intersect_x, self.intersect_y = self.calculate_axes_intersections()
        self.equation = self.calculate_equation()
        self.angle = self.calculate_angle()
        self.setPos(self.intersect_x)
        self.setAngle(self.angle)

    def calculate_axes_intersections(self) -> Tuple[QPointF, QPointF]:
        y_coefficient = self.function[self.index_y]
        x_coefficient = self.function[self.index_x]
        x_part = self.function[0] / x_coefficient if x_coefficient != 0 else 0
        y_part = self.function[0] / y_coefficient if y_coefficient != 0 else 0
        return QPointF(x_part, 0), QPointF(0, y_part)

    def calculate_equation(self):
        gradient = (self.intersect_y.y() - self.intersect_x.y()) / (self.intersect_y.x() - self.intersect_x.x()) if self.intersect_x.x() - self.intersect_y.x() != 0 else 0
        constant = self.intersect_x.y() - gradient * self.intersect_x.x()
        return gradient, constant


def get_lines_intersection(lhs: Line2D, rhs: Line2D) -> QPointF | None:
    if lhs.equation[0] == rhs.equation[0]:
        return
    x_inter = (lhs.equation[1] - rhs.equation[1]) / (rhs.equation[0] - lhs.equation[0])
    y_inter = x_inter * lhs.equation[0] + lhs.equation[1]
    return QPointF(x_inter, y_inter)
