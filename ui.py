from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt
from canvas import Canvas


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Model Viewer")
        self.setGeometry(100, 100, 1000, 600)

        # Основной виджет и компоновка
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Создаём канвас для отображения модели
        self.canvas = Canvas(800, 600, self)
        main_layout.addWidget(self.canvas)

        # Панель управления с ползунками
        controls_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)

        # Ползунок для вращения по оси X
        self.x_slider = self.create_slider("Поворот вокруг Ox", controls_layout, self.update_x_rotation)

        # Ползунок для вращения по оси Y
        self.y_slider = self.create_slider("Поворот вокруг Ox", controls_layout, self.update_y_rotation)

        # Ползунок для вращения по оси Z
        self.z_slider = self.create_slider("Поворот вокруг Ox", controls_layout, self.update_z_rotation)

        # Настройка значений ползунков
        self.reset_sliders()

    def create_slider(self, label_text, layout, callback):
        """
        Создаёт ползунок с подписью и добавляет его в указанную компоновку.
        """
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(-180)
        slider.setMaximum(180)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.valueChanged.connect(callback)  # Подключаем обработчик изменений значения
        layout.addWidget(slider)

        return slider

    def update_x_rotation(self, value):
        """
        Обработчик для вращения по оси X.
        """
        self.canvas.current_angles["x"] = value
        self.canvas.draw_model()

    def update_y_rotation(self, value):
        """
        Обработчик для вращения по оси Y.
        """
        self.canvas.current_angles["y"] = value
        self.canvas.draw_model()

    def update_z_rotation(self, value):
        """
        Обработчик для вращения по оси Z.
        """
        self.canvas.current_angles["z"] = value
        self.canvas.draw_model()

    def reset_sliders(self):
        """
        Устанавливает ползунки в начальное положение (0 градусов).
        """
        self.x_slider.setValue(0)
        self.y_slider.setValue(0)
        self.z_slider.setValue(0)
