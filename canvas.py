from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QPainter
from PyQt5.QtCore import Qt, QPointF
from geometry import Geometry

class Canvas(QGraphicsView):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Исправлено использование Antialiasing
        self.setRenderHint(QPainter.Antialiasing)

        self.geometry = Geometry()

        self.setFixedSize(width, height)
        self.setSceneRect(-width // 2, -height // 2, width, height)

        self.current_angles = {"x": 0, "y": 0, "z": 0}
        self.last_mouse_position = None

        self.draw_model()

    def draw_model(self):
        self.scene.clear()
        for face in self.geometry.get_visible_faces(self.current_angles):
            polygon = QPolygonF([QPointF(x, y) for x, y in face])
            self.scene.addPolygon(polygon, QPen(Qt.blue), QBrush(Qt.green))

    def rotate_model(self, dx, dy, dz=0):
        self.current_angles["x"] += dx
        self.current_angles["y"] += dy
        self.current_angles["z"] += dz
        self.draw_model()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_position:
            dx = event.x() - self.last_mouse_position.x()
            dy = event.y() - self.last_mouse_position.y()
            self.rotate_model(dy, -dx)
            self.last_mouse_position = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_position = None
