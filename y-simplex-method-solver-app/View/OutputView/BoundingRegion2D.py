from pyqtgraph import GraphicsObject, mkPen, mkBrush
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPolygonF, QPainter, QPicture
from PyQt6.QtCore import QPointF, QRectF
from typing import List


class BoundingRegion2D(GraphicsObject):
    def __init__(self, parent: QWidget | None = None, points: List[QPointF] | None = None):
        super().__init__()
        self.parent = parent
        self.points = points
        self.bounding_region = QPolygonF()
        self.picture = QPicture()
        self.update_points()

    def update_points(self):
        self.bounding_region.clear()
        if self.points is not None and len(self.points) > 2:
            for i in self.points:
                self.bounding_region.append(i)
            self.generate_picture()

    def set_points(self, points: List[QPointF]):
        self.points = points
        self.update_points()

    def generate_picture(self):
        painter = QPainter(self.picture)
        painter.setPen(mkPen((10, 10, 255, 175)))
        painter.setBrush(mkBrush((10, 10, 255, 175)))
        painter.drawPolygon(self.bounding_region)
        painter.end()

    def paint(self, painter, option, widget=None):
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())
