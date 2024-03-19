import time
from datetime import datetime

from PySide2.QtCore import QTimer
from PySide2.QtGui import Qt, QFont
from PySide2.QtWidgets import QWidget, QFileDialog, QGridLayout
from pages.page_generate_file import GeneratePageWindow
from pages.page_show_result import ResultWindow
from utils import (morse_to_text,
                   create_textfield,
                   create_button,
                   create_button_by_cls,
                   create_label,
                   Timer, CustomPushButton)


class MainWindow(QWidget):
    def __init__(self):
        """ Класс для создания и отображения основного окна программы"""
        super().__init__()
        self.setWindowTitle("Основное меню")  # присваивает окну название
        # self.setFixedSize(780, 560)  # задает размер окна
        self.setMinimumWidth(600)

        self.timer_for_label = Timer()

        self.last_time_button_pressed = 0  # время последнего нажатия кнопки
        self.key_press_time = None  # время зажатия кнопки

        self.start_time = 0  # время счетчика
        # Таймер
        self.timer = QTimer()
        self.timer.timeout.connect(
            self.update_time
        )  # тут связываем с функцией для обновления раз в секунду
        self.timer.start(1000)  # тут задаем ему скорость
        self.timer_label = create_label(
            self,
            text="00:00",
            font_size=15,
            center=True
        )  # вот тут создаю лейбл для таймера
        self.timer_label.setStyleSheet(
            ("QLabel {"
             " background-color: #FF0000;"
             " color: #FFFFFF;"
             " border: 2px solid #000000;"
             "}"))

        self.button_open_file = create_button(
            self,
            name="Открыть файл",
            func=self.read_file,
        )
        self.button_create_file = create_button(
            self,
            name="Сгенерировать",
            func=self.generate_new_file,
        )
        self.button_make_check = create_button(
            self,
            name="Проверить",
            func=self.return_result,
        )
        self.button_stop = create_button(
            self,
            name="Стоп",
            func=self.stop_timer,
        )
        self.button_start = create_button(
            self,
            name="Старт",
            func=self.start_timer,
        )

        self.button_key = create_button(self, name="Ключ", func=None)
        self.button_key.setFont(QFont('Times', 15))
        self.button_key.setStyleSheet("QPushButton {background-color: blue; color: white; border: 1px solid; border-radius: 2px; }")

        self.text_filed_task = create_textfield(self)

        self.text_filed_translate = create_textfield(self)

        self.text_filed_morse = create_textfield(self, func=self.on_text_changed)

        # add all objects to grid LAYOUT
        self.grid = QGridLayout()  # создаем грид для отображения объектов в окне

        self.grid.addWidget(self.timer_label, 0, 0)  # добавляем таймер в первый столбец первую строку

        self.grid.addWidget(self.button_open_file, 1, 0)  # добавляем кнопку в 1 и 2 столбец вторая строка
        self.grid.addWidget(self.button_create_file, 1, 1)  # добавляем кнопку в 3 и 4 столбец вторая строка
        self.grid.addWidget(self.button_make_check, 1, 2)  # добавляем кнопку в 5, 6 и 7 столбец вторая строка
        self.grid.addWidget(self.button_stop, 1, 3)  # добавляем кнопку в 8 и 9 столбец вторая строка
        self.grid.addWidget(self.button_start, 1, 4)  # добавляем кнопку в 10, 11 столбец вторая строка

        self.grid.addWidget(self.button_key, 2, 0, 1, 5)

        self.grid.addWidget(self.text_filed_task, 3, 0, 1, 5)  # добавляем лэйбл текст во всю 3 и 4 строки
        self.grid.addWidget(self.text_filed_translate, 4, 0, 1, 5)  # добавляем лэйбл текст во всю 5 и 6 строки
        self.grid.addWidget(self.text_filed_morse, 5, 0, 1, 5)  # добавляем лэйбл текст во всю 7 и 8 строки

        self.grid.setRowMinimumHeight(1, 60)
        self.grid.setRowMinimumHeight(2, 60)

        # Set stretch factors for rows
        self.grid.setRowStretch(0, 1)  # Timer row
        self.grid.setRowStretch(1, 1)  # Buttons row
        self.grid.setRowStretch(2, 2)  # Key Button row
        self.grid.setRowStretch(3, 3)  # Task text row
        self.grid.setRowStretch(4, 3)  # Translate text row
        self.grid.setRowStretch(5, 3)  # Morse code row

        self.setLayout(self.grid)

    def update_time(self):
        minutes, seconds = divmod(self.timer_for_label.get_elapsed_time(), 60)
        self.timer_label.setText(f"{int(minutes):02d}:{int(seconds):02d}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            if self.last_time_button_pressed != 0:
                if time.time() - self.last_time_button_pressed > 1.05:
                    if self.text_filed_morse.toPlainText()[-1] != "   ":
                        self.text_filed_morse.setText(
                            self.text_filed_morse.toPlainText() + "  ")
                elif time.time() - self.last_time_button_pressed > 0.45:
                    if len(self.text_filed_morse.toPlainText()[-1]) > 0 and \
                            self.text_filed_morse.toPlainText()[-1] != " ":
                        self.text_filed_morse.setText(
                            self.text_filed_morse.toPlainText() + " ")
        self.key_press_time = time.time()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W and not event.isAutoRepeat():
            self.last_time_button_pressed = time.time()
            total_push_time = self.last_time_button_pressed - self.key_press_time
            if 0.15 < total_push_time <= 0.45:
                self.text_filed_morse.setText(
                    self.text_filed_morse.toPlainText() + "-")
            elif total_push_time <= 0.15:
                self.text_filed_morse.setText(
                    self.text_filed_morse.toPlainText() + ".")

    def on_text_changed(self):
        self.text_filed_translate.setText(
            morse_to_text(
                self.text_filed_morse.toPlainText()
            )
        )

    def generate_new_file(self):
        self.new_window = GeneratePageWindow()
        self.new_window.show()

    def read_file(self):
        self.text_filed_translate.setStyleSheet(
            "QTextEdit {border: 3px solid #1966FF; }")
        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            with open(filename, 'r') as f:
                data = f.read()
            self.text_filed_task.setText(data)

    def return_result(self):
        minutes, seconds = divmod(self.timer_for_label.get_elapsed_time(), 60)
        data = {
            "time": (minutes, int(seconds)),
            "initial_text": self.text_filed_task.toPlainText(),
            "verifiable_text": self.text_filed_translate.toPlainText(),
        }
        self.result_window = ResultWindow(data=data)
        self.text_filed_translate.setText(
            self.result_window.show_mistakes(data=data)
        )
        self.result_window.show()
        self.timer_for_label.reset()

    def start_timer(self):
        if self.text_filed_task.toPlainText() == "":
            print("Выберите задание")
            return
        self.timer_for_label.start()
        self.start_time = datetime.now()
        self.text_filed_morse.setText("")
        self.text_filed_translate.setText('')
        self.last_time_button_pressed = 0

    def stop_timer(self):
        self.timer_for_label.stop()
