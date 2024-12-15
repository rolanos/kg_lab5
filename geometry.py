import numpy as np
from math import cos, sin, radians, sqrt

class Geometry:
    def __init__(self):
        self.vertices = np.array([
            [-50, 50, -50],  # Пересчитано относительно центра (0, 0, 0)
            [50, 50, -50],
            [50, -50, -50],
            [-50, -50, -50],
            [-50, 50, 50],
            [50, 50, 50],
            [50, -50, 50],
            [-50, -50, 50]
        ])

        self.faces = [
            (0, 1, 2, 3), (5, 4, 7, 6),
            (4, 0, 3, 7), (1, 5, 6, 2),
            (4, 5, 1, 0), (3, 2, 6, 7)
        ]
        self.face_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255)
        ]

        self.light_position = np.array([0, 0, -500])  # Положение источника света
        self.camera_position = np.array([0, 0, -500])  # Положение камеры

    def rotate_vertex(self, vertex, angles):
        x, y, z = vertex
        rx, ry, rz = radians(angles["x"]), radians(angles["y"]), radians(angles["z"])

        rotation_x = np.array([
            [1, 0, 0],
            [0, cos(rx), -sin(rx)],
            [0, sin(rx), cos(rx)]
        ])
        rotation_y = np.array([
            [cos(ry), 0, sin(ry)],
            [0, 1, 0],
            [-sin(ry), 0, cos(ry)]
        ])
        rotation_z = np.array([
            [cos(rz), -sin(rz), 0],
            [sin(rz), cos(rz), 0],
            [0, 0, 1]
        ])
        rotated = np.dot(rotation_z, np.dot(rotation_y, np.dot(rotation_x, [x, y, z])))
        return rotated

    def normalize(self, vector):
        norm = sqrt(sum(v**2 for v in vector))
        return vector / norm if norm != 0 else vector

    def compute_lambertian_intensity(self, normal, light_direction):
        #Вычисляем интенсивность освещения по модели Ламберта.
        intensity = max(np.dot(normal, light_direction), 0)  # Учитываем только положительное значение
        return intensity

    def is_face_visible(self, normal, camera_direction):
        #Проверяет, видима ли грань с точки зрения камеры.
        return np.dot(normal, camera_direction) > 0

    def get_visible_faces(self, angles):
        rotated_vertices = [self.rotate_vertex(v, angles) for v in self.vertices]
        visible_faces = []

        light_direction = self.normalize(self.light_position)
        camera_direction = self.normalize(self.camera_position)

        for face_index, face in enumerate(self.faces):
            a, b, c, d = [rotated_vertices[i] for i in face]
            normal = np.cross(np.array(b) - np.array(a), np.array(c) - np.array(a))
            normal = self.normalize(normal)

            if self.is_face_visible(normal, camera_direction):  # Учитываем видимость с точки зрения камеры
                intensity = self.compute_lambertian_intensity(normal, light_direction)
                adjusted_intensity = max(intensity, 0.2)  # Минимальная яркость для затемнённых граней
                color = self.adjust_color_brightness(self.face_colors[face_index], adjusted_intensity)
                visible_faces.append({
                    "vertices": [(a[0], a[1]), (b[0], b[1]), (c[0], c[1]), (d[0], d[1])],
                    "color": color
                })
        return visible_faces

    def adjust_color_brightness(self, color, intensity):
        #Модифицируем яркость цвета в зависимости от интенсивности света.
        return tuple(min(255, max(0, int(c * intensity))) for c in color)
