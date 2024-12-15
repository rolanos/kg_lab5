from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF
from geometry import Geometry  # Убедитесь, что импортируете класс Geometry


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

        # Отображаем сам многогранник
        for face in self.geometry.get_visible_faces(self.current_angles):
            polygon = QPolygonF([QPointF(x, y) for x, y in face["vertices"]])
            self.scene.addPolygon(polygon, QPen(Qt.blue), QBrush(QColor(*face["color"])))

        # Убираем отображение точки источника света
        # self.draw_light_source()

    def draw_light_source(self):
        # Позиция источника света в мировых координатах
        light_pos = self.geometry.light_position
        light_x, light_y, light_z = light_pos[0], light_pos[1], light_pos[2]

        # Схематично рисуем точку источника света как маленький круг
        # Преобразуем мировые координаты в координаты канвы
        # Для этого учитываем текущие масштабы и преобразования
        light_screen_pos = QPointF(light_x, light_y)

        # Добавляем маленькую точку на сцену
        self.scene.addEllipse(light_screen_pos.x() - 5, light_screen_pos.y() - 5, 10, 10,
                              QPen(Qt.red), QBrush(Qt.red))  # Красная точка источника света

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
