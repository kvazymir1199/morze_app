from PySide2.QtWidgets import QApplication
from pages.page_main import MainWindow
from pages.page_generate_file import GeneratePageWindow

app = QApplication([])
new_window = GeneratePageWindow()
window = MainWindow()
window.show()
app.exec_()
