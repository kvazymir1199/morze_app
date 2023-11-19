from PySide2.QtWidgets import QWidget
from utils import create_label


def return_mistakes_count(data: dict):
    """ Функция проверки ошибок. Для сравнения берутся строка из файла
    задания и строка переведенная с кода морзе"""
    count = 0
    for item1, item2 in zip(data.get("initial_text"),
                            data.get("verifiable_text")):
        if item1 != item2:
            count += 1
    return count


def return_speed_printing(data: dict):
    """ Функция расчета времени печати по формуле
    длинна передаваемой строки / время с начала запуска """
    length = len(data.get('verifiable_text'))
    time_in_seconds = data.get('time')[0] * 60 + data.get('time')[1]
    return round(length / time_in_seconds, 2)


class ResultWindow(QWidget):
    """ Класс для отображения результатов тренажера"""

    def __init__(self, data: dict):
        super().__init__()
        self.setWindowTitle("Ваш результат")
        self.setFixedSize(350, 170)
        # ----------------------------------------------------------------
        # Графическая метка отображения скорости печати
        self.label_show_speed = create_label(
            self,
            text="Скорость - ",
            x=10,
            y=10
        )
        self.label_digits_in_minute = create_label(
            self,
            text=f"{return_speed_printing(data)} зн/мин",
            x=200,
            y=10
        )
        #  ----------------------------------------------------------------
        # Графическая метка отображения полученных ошибок
        self.label_mistakes_count = create_label(
            self,
            text="Кол. ошибок - ",
            x=10,
            y=50
        )
        self.label_mistakes_count = create_label(
            self,
            text=f"{return_mistakes_count(data)}",
            x=200,
            y=50
        )
        # ----------------------------------------------------------------
        # Графическая метка отображения времени
        self.label_current_time = create_label(
            self,
            text="Время - ",
            x=10,
            y=100
        )
        minutes, seconds = divmod(data["time"][1], 60)
        self.label_show_time = create_label(
            self,
            text=f"{minutes:02d}:{seconds:02d}",
            x=200,
            y=100
        )
