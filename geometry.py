import numpy as np
from math import cos, sin, radians

class Geometry:
    def __init__(self):
        self.vertices = np.array([
            [100, 100, 0], [200, 100, 0], [200, 0, 0], [100, 0, 0],
            [100, 100, 100], [200, 100, 100], [200, 0, 100], [100, 0, 100]
        ])
        self.faces = [
            (0, 1, 2, 3), (5, 4, 7, 6),
            (4, 0, 3, 7), (1, 5, 6, 2),
            (4, 5, 1, 0), (3, 2, 6, 7)
        ]

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

    def get_visible_faces(self, angles):
        rotated_vertices = [self.rotate_vertex(v, angles) for v in self.vertices]
        visible_faces = []
        for face in self.faces:
            a, b, c, d = [rotated_vertices[i] for i in face]
            normal = np.cross(np.array(b) - np.array(a), np.array(c) - np.array(a))
            if normal[2] > 0:  # Simple visibility check
                visible_faces.append([(a[0], a[1]), (b[0], b[1]), (c[0], c[1]), (d[0], d[1])])
        return visible_faces
