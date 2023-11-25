from PySide2.QtWidgets import QApplication
from pages.page_main import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
