import os
import random

from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QWidget, QLabel, QLineEdit, QFileDialog,
                               QPushButton, QComboBox, QTextEdit)

STRING_LENGTH = 5
RUSSIAN_LETTERS = [chr(i) for i in range(1072, 1104)]
DIGITS = list(map(str, range(10)))
STRING_TOTAL_LENGTH_IN_TEXT_EDIT = 599  # 100 групп * 5 символов + максимум 99 пробелов


class GeneratePageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генерация файла")
        self.setFixedSize(400, 290)

        self.label = QLabel("Количество групп", self)
        self.label.move(10, 10)
        self.label.setFont(QFont('Arial', 10))

        self.text_field_group = QLineEdit(self)
        self.text_field_group.move(130, 10)
        self.text_field_group.setFixedSize(40, 20)

        self.label = QLabel("Формат текста", self)
        self.label.move(180, 10)
        self.label.setFont(QFont('Arial', 10))

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("цифровой")
        self.combo_box.addItem("буквенный")
        self.combo_box.move(270, 10)

        self.text_field = QTextEdit(self)
        self.text_field.move(10, 50)
        self.text_field.setFixedSize(380, 200)
        self.text_field.setStyleSheet(
            "QTextEdit {border: 3px solid #1966FF; }")

        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_text_to_file)
        self.save_button.move(270, 255)

        self.save_button = QPushButton("Сгенерировать", self)
        self.save_button.clicked.connect(
            lambda: self.generate_random_string(self.text_field_group.text(),
                                                self.combo_box.currentText()))
        self.save_button.move(70, 255)

    def save_text_to_file(self):
        text = self.text_field.toPlainText()
        filename = QFileDialog.getSaveFileName(self, "Save file",
                                               os.path.expanduser("~/Desktop"))
        if filename[0]:
            with open(filename[0], 'w') as f:
                f.write(text)

    def generate_random_string(self, words_amount, text_type):
        if not (words_amount.isdigit() and 1 <= int(words_amount) <= 100):
            print("Укажите цифровое значение от 1-100")
            return
        text = ""
        string_base = (RUSSIAN_LETTERS, DIGITS)[text_type == 'цифровой']

        for x in range(0, int(words_amount)):
            text += "".join(
                random.choice(string_base) for i in range(STRING_LENGTH))
            text += " "

        self.text_field.setText(text)
        return text
