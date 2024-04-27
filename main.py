import os

from PySide2.QtWidgets import QApplication
from pages.page_main import MainWindow


if __name__ == '__main__':
    app = QApplication([])
    current_dir = os.path.dirname(os.path.abspath(__file__))
    window = MainWindow(current_dir)
    window.show()
    app.exec_()
