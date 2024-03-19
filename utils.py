import random
import time
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTextEdit, QPushButton, QLabel, QSizePolicy
from PySide2.QtCore import QElapsedTimer, Qt

MORSE_CODE_DICT = {'а': '.-', 'б': '-...', 'в': '.--', 'г': '--.', 'д': '-..',
                   'е': '.', 'ж': '...-', 'з': '--..',
                   'и': '..', 'й': '.---', 'к': '-.-', 'л': '.-..', 'м': '--',
                   'н': '-.', 'о': '---', 'п': '.--.',
                   'р': '.-.', 'с': '...', 'у': '..-', 'ф': '..-.',
                   'х': '....', 'ц': '-.-.', 'ч': '---.',
                   'ш': '----', 'щ': '--.-', 'ъ': '--.--', 'ы': '-.--',
                   'ь': '-..-', 'э': '..-..', 'ю': '..--', 'я': '.-.-',
                   '0': '-', '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....', '7': '--...',
                   '8': '---..', '9': '----.', '   ': '',
                   }
RUSSIAN_LETTERS = [chr(i) for i in range(1072, 1104)]
DIGITS = list(map(str, range(10)))
STRING_LENGTH = 5


def create_textfield(parent, func=None):
    """Функция для создания текстового поля"""
    label = QTextEdit(parent=parent)
    label.setReadOnly(True)
    label.setStyleSheet("QTextEdit {border: 3px solid #1966FF; ; border-radius: 3px;}")
    label.textChanged.connect(func)
    return label


def create_button(parent, name, func):
    """Функция для создания кнопки"""
    button = QPushButton(name, parent=parent)
    if func is not None:
        button.clicked.connect(func)
    button.setStyleSheet("QPushButton {border: 1px solid; border-radius: 2px;}")
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return button


def create_button_by_cls(parent, cls, name, func):
    """Функция для создания кнопки любого типа"""
    button = cls(name, parent=parent)
    if func is not None:
        button.clicked.connect(func)
    button.setStyleSheet("QPushButton {border: 1px solid; border-radius: 3px;}")
    return button


def create_label(self, text, font_size=20, center: bool = False):
    """Функция для создания текстовой метки"""
    label = QLabel(self)
    label.setFont(QFont('Arial', font_size))
    label.setText(text)
    if center:
        label.setAlignment(Qt.AlignCenter)
    return label


def morse_to_text(morse):
    """Функция для преобразования текста в код морзе"""
    morse = morse.split(' ')
    text = ''
    for symbol in morse:
        for letter, code in MORSE_CODE_DICT.items():
            if symbol == code:
                text += letter
    return text


def generate_random_string(self, words_amount, text_type):
    """Функция для создания строки состоящей из групп по 5 символов"""
    if not (words_amount.isdigit() and 1 <= int(words_amount) <= 100):
        print("Укажите цифровое значение от 1-100")
        return

    # Определение доступных символов
    string_base = {
        'цифровой': DIGITS,
        'буквенный': RUSSIAN_LETTERS
    }

    # Проверка наличия нужного типа текста
    if text_type not in string_base:
        print("Недопустимый тип текста")
        return

    text = ""
    prev_char = None  # Хранение предыдущего символа

    for _ in range(int(words_amount)):
        word = ""
        while len(word) < 5:
            char = random.choice(string_base[text_type])

            # Проверка на повторение символов
            if char != prev_char:
                word += char
                prev_char = char

        text += word + "   "

    self.text_field.setText(text)
    return text


class CustomPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(CustomPushButton, self).__init__(*args, **kwargs)
        self.timer = QElapsedTimer()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.timer.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            duration = self.timer.elapsed()
            print(f"Duration of left mouse button press: {duration} ms")
        super().mouseReleaseEvent(event)


class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()

    def stop(self):
        if self.is_running:
            self.is_running = False
            end_time = time.time()
            self.elapsed_time += end_time - self.start_time

    def reset(self):
        self.is_running = False
        self.elapsed_time = 0

    def get_elapsed_time(self):
        if self.is_running:
            return self.elapsed_time + time.time() - self.start_time
        return self.elapsed_time
