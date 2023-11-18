# from PySide2.QtWidgets import QApplication, QMainWindow
# from PySide2.QtCore import Qt
# import time
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.last_key_press_time = None
#
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_W and not event.isAutoRepeat():
#             if self.last_key_press_time is not None:
#                 print(time.time() - self.last_key_press_time)
#             self.last_key_press_time = time.time()
#             self.key_press_time = time.time()
#
#     def keyPressEventW(self, event):
#         if event.key() == Qt.Key_W:
#             self.key_press_time = time.time()
#
#     def keyReleaseEventW(self, event):
#         if event.key() == Qt.Key_W and not event.isAutoRepeat():
#             end = time.time()
#             print(end - self.key_press_time)
#
#
# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec_()

# from PySide2.QtWidgets import QApplication, QMainWindow
# from PySide2.QtCore import Qt
# import time
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.key_press_time = None
#
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_W:
#             self.key_press_time = time.time()
#
#     def keyReleaseEvent(self, event):
#         if event.key() == Qt.Key_W and not event.isAutoRepeat():
#             end = time.time()
#             print(end - self.key_press_time)
#
#
# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec_()

# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication, QWidget
# import time
#
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Key Events")
#         self.setGeometry(100, 100, 300, 200)
#
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_W:
#             print("Клавиша W нажата")
#             # Дополнительные действия при необходимости
#             self.key_press_time = time.time()
#
#     def keyReleaseEvent(self, event):
#         if event.key() == Qt.Key_W and not event.isAutoRepeat():
#             print("Клавиша W отпущена")
#             # Дополнительные действия при необходимости
#             end = time.time()
#             print(end - self.key_press_time)  # Вычисление разницы во времени
#
#
# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec_()

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget
import time


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Key Events")
        self.setGeometry(100, 100, 300, 200)
        self.key_timer = QTimer(self)
        self.key_timer.setInterval(
            500)  # Интервал для определения удержания клавиши
        self.key_timer.timeout.connect(self.check_key_held)
        self.key_is_pressed = False
        self.key_press_time = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W and not self.key_is_pressed:
            print("Клавиша W нажата")
            self.key_is_pressed = True
            self.key_press_time = time.time()
            self.key_timer.start()  # Запуск таймера для проверки удержания клавиши

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W and self.key_is_pressed:
            print("Клавиша W отпущена")
            self.key_is_pressed = False
            self.key_timer.stop()  # Остановка таймера при отпускании клавиши
            end = time.time()
            print(end - self.key_press_time)

    def check_key_held(self):
        print("Клавиша W удерживается")


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
