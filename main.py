from PyQt5.QtWidgets import QApplication
from ui import AppWindow
import sys

def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
