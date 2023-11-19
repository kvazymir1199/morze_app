# Словарь для азбуки Морзе
import random

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTextEdit, QPushButton, QLabel

MORSE_CODE_DICT = {'а': '.-', 'б': '-...', 'в': '.--', 'г': '--.', 'д': '-..',
                   'е': '.', 'ж': '...-', 'з': '--..',
                   'и': '..', 'й': '.---', 'к': '-.-', 'л': '.-..', 'м': '--',
                   'н': '-.', 'о': '---', 'п': '.--.',
                   'р': '.-.', 'с': '...', 'т': '-', 'у': '..-', 'ф': '..-.',
                   'х': '....', 'ц': '-.-.', 'ч': '---.',
                   'ш': '----', 'щ': '--.-', 'ъ': '--.--', 'ы': '-.--',
                   'ь': '-..-', 'э': '..-..', 'ю': '..--', 'я': '.-.-',
                   '0': '-----', '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....', '7': '--...',
                   '8': '---..', '9': '----.', '   ': '',
                   }
RUSSIAN_LETTERS = [chr(i) for i in range(1072, 1104)]
DIGITS = list(map(str, range(10)))
STRING_LENGTH = 5


def morse_to_text(morse):
    morse = morse.split(' ')
    text = ''
    for symbol in morse:
        for letter, code in MORSE_CODE_DICT.items():
            if symbol == code:
                text += letter
    return text


def create_textfield(self, x=0, y=0, length=0, width=0, func=None):
    label = QTextEdit(self)
    label.setReadOnly(True)
    label.move(x, y)
    label.setFixedSize(length, width)
    label.setStyleSheet("QTextEdit {border: 3px solid #1966FF; }")
    label.textChanged.connect(func)
    return label


def create_button(self, name, func, x, y, length=100, width=30):
    self.button = QPushButton(name, self)
    self.button.clicked.connect(func)
    self.button.move(x, y)
    self.button.resize(length, width)
    return self.button


def create_label(self, text, x, y, font_size=20):
    label = QLabel(self)
    label.move(x, y)
    label.setFont(QFont('Arial', font_size))
    label.setText(text)
    return label


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
