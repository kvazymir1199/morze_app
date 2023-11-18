import time
from datetime import datetime

from PySide2.QtCore import QTimer
from PySide2.QtGui import QFont, Qt
from PySide2.QtWidgets import (QApplication, QWidget, QHBoxLayout, QFileDialog,
                               QLabel, QTextEdit)

from pages.page_generate_file import GeneratePageWindow
from pages.page_show_result import ResultWindow
from PySide2.QtWidgets import QPushButton
from utils import morse_to_text

BUTTON_SIZE = (150, 50)
layout = (15, 50)
SHIFT_BUTTON = 0
TEXTFIELD_SIZE = (750, 120)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.last_time_button_pressed = 0  # время последнего нажатия кнопки
        self.key_press_time = None  # время зажатия кнопки
        self.setWindowTitle("Основное меню")  # присваивает окну название
        self.setFixedSize(780, 560)  # задает размер окна
        self.start_time = 0  # время счетчика
        # Таймер
        self.label = QLabel("00:00", self)  # лейбл для счетчика
        # Устанавливаем координаты относительно основного окна
        self.label.move(layout[0], 10)
        self.label.setFont(QFont('Arial', 15))
        self.label.setStyleSheet(
            "QLabel { background-color: #FF0000; color: #FFFFFF; border: 2px solid #000000; }")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.button = self.create_button(
            name="Открыть файл",
            func=self.read_file,
            x=layout[0],
            y=layout[1],
            height=BUTTON_SIZE[0],
            width=BUTTON_SIZE[1]
        )
        self.button = self.create_button(
            name="Генерация файла",
            func=self.generate_new_file,
            x=layout[0] + BUTTON_SIZE[0] + SHIFT_BUTTON,
            y=layout[1],
            height=BUTTON_SIZE[0],
            width=BUTTON_SIZE[1]
        )
        self.button = self.create_button(
            name="Выполнить проверку",
            func=self.return_result,
            x=layout[0] + (BUTTON_SIZE[0] + SHIFT_BUTTON) * 2,
            y=layout[1],
            height=BUTTON_SIZE[0] * 2,
            width=BUTTON_SIZE[1]
        )
        self.button = self.create_button(
            name="Стоп",
            func=self.stop_timer,
            x=layout[0] + (BUTTON_SIZE[0] + SHIFT_BUTTON) * 4,
            y=layout[1],
            height=BUTTON_SIZE[0] // 2,
            width=BUTTON_SIZE[1]
        )
        self.button = self.create_button(
            name="Старт",
            func=self.start_timer,
            x=layout[0] + (BUTTON_SIZE[0] + SHIFT_BUTTON) * 4.5,
            y=layout[1],
            height=BUTTON_SIZE[0] // 2,
            width=BUTTON_SIZE[1]
        )
        self.label_task_text = self.create_label(layout[0], 140)

        self.label_text_translate = self.create_label(layout[0], 280)

        self.label_morse_code = self.create_label(
            layout[0],
            420,
            self.on_text_changed
        )

    def create_label(self, x, y, func=None):
        label = QTextEdit(self)
        label.setReadOnly(True)
        label.move(x, y)
        label.setFixedSize(*TEXTFIELD_SIZE)
        label.setStyleSheet("QTextEdit {border: 3px solid #1966FF; }")
        label.textChanged.connect(func)
        return label

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            if self.last_time_button_pressed != 0:
                if time.time() - self.last_time_button_pressed > 2:
                    if self.label_morse_code.toPlainText()[-1] != "   ":
                        self.label_morse_code.setText(
                            self.label_morse_code.toPlainText() + "  ")
                elif time.time() - self.last_time_button_pressed > 0.7:
                    if len(self.label_morse_code.toPlainText()[-1]) > 0 and \
                            self.label_morse_code.toPlainText()[-1] != " ":
                        self.label_morse_code.setText(
                            self.label_morse_code.toPlainText() + " ")
            print("Клавиша нажата")
        self.key_press_time = time.time()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W and not event.isAutoRepeat():
            print("Клавиша отпущена")
            self.last_time_button_pressed = time.time()
            total_push_time = self.last_time_button_pressed - self.key_press_time
            if 0.15 < total_push_time <= 0.70:
                self.label_morse_code.setText(
                    self.label_morse_code.toPlainText() + "-")
            elif total_push_time <= 0.15:
                self.label_morse_code.setText(
                    self.label_morse_code.toPlainText() + ".")

    def on_text_changed(self):
        self.label_text_translate.setText(
            morse_to_text(self.label_morse_code.toPlainText()))

    def create_button(self, name, func, x, y, height, width):
        self.button = QPushButton(name, self)
        self.button.clicked.connect(func)
        self.button.move(x, y)
        self.button.resize(height, width)
        return self.button

    def update_time(self):
        if self.start_time == 0:
            return
        elapsed_time = datetime.now() - self.start_time
        minutes, seconds = divmod(elapsed_time.seconds, 60)
        self.label.setText(f"{minutes:02d}:{seconds:02d}")

    def generate_new_file(self):
        self.new_window = GeneratePageWindow()
        self.new_window.show()

    def read_file(self):

        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            with open(filename, 'r') as f:
                data = f.read()
            self.label_task_text.setText(data)

    def return_result(self):
        if self.start_time == 0:
            return
        elapsed_time = datetime.now() - self.start_time
        minutes, seconds = divmod(elapsed_time.seconds, 60)
        data = {
            "time": (minutes, seconds),
            "initial_text": self.label_task_text.toPlainText(),
            "verifiable_text": self.label_text_translate.toPlainText(),
        }
        self.new_window = ResultWindow(data=data)
        self.new_window.show()
        self.start_time = 0

    def start_timer(self):
        if self.label_task_text.toPlainText() == "":
            print("Выберите задание")
            return
        self.timer.start()
        self.start_time = datetime.now()
        self.label_morse_code.setText("")
        self.label_text_translate.setText('')
        self.last_time_button_pressed = 0

    def stop_timer(self):
        self.timer.stop()
