from PySide2.QtWidgets import QApplication
from pages.page_main import MainWindow


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
