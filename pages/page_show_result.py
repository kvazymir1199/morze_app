from PySide2.QtWidgets import QWidget, QGridLayout, QSizePolicy
from utils import create_label


def return_mistakes_count_1(data: dict):
    """ Функция проверки ошибок. Для сравнения берутся строка из файла
    задания и строка переведенная с кода морзе"""
    count = 0
    mistakes = ""
    for item1, item2 in zip(data.get("initial_text"),
                            data.get("verifiable_text")):

        if item1 != item2:
            mistakes += item2 + " "
            count += 1
    return count


def return_mistakes_count(data: dict):
    count = 0
    item_2: str = data.get("verifiable_text")
    if item_2 == "" or data.get('time')[0] * 60 + data.get('time')[1] == 0:
        return 0

    first_array: str = data.get("initial_text").split("   ")
    second_array: str = data.get("verifiable_text").split("   ")

    for item1, item2 in zip(first_array, second_array):
        for base_letter, input_letter in zip(item2, item1):
            if base_letter != input_letter:
                count += 1

        difference = abs(len(item1) - len(item2))
        if difference != 0:
            count += abs(difference)

    return count


def return_speed_printing(data: dict):
    """ Функция расчета времени печати по формуле
    длинна передаваемой строки / время с начала запуска """
    length = len(data.get('verifiable_text').replace(' ', ''))
    time_in_seconds = (data.get('time')[0] * 60 + data.get('time')[1]) / 60
    try:
        return round(length / time_in_seconds, 2)
    except ZeroDivisionError:
        return 0


class ResultWindow(QWidget):
    """ Класс для отображения результатов тренажера"""

    def __init__(self, data: dict):
        super().__init__()
        self.setWindowTitle("Ваш результат")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # ----------------------------------------------------------------
        # Графическая метка отображения скорости печати
        self.label_show_speed = create_label(
            self,
            text="Скорость - ",
            # x=10,
            # y=10
        )
        self.label_digits_in_minute = create_label(
            self,
            text=f"{return_speed_printing(data)} зн/мин",
            # x=200,
            # y=10
        )
        #  ----------------------------------------------------------------
        # Графическая метка отображения полученных ошибок
        self.label_mistakes_count = create_label(
            self,
            text="Кол. ошибок - ",
            # x=10,
            # y=50
        )
        self.label_mistakes_count_ = create_label(
            self,
            text=f"{return_mistakes_count(data)}",
            # x=200,
            # y=50
        )
        # ----------------------------------------------------------------
        # Графическая метка отображения времени
        self.label_current_time = create_label(
            self,
            text="Время - ",
            # x=10,
            # y=100
        )
        minutes, seconds = divmod(data["time"][0] * 60 + data["time"][1], 60)
        self.label_show_time = create_label(
            self,
            text=f"{int(minutes):02d}:{int(seconds):02d}",
            # x=200,
            # y=100
        )

        self.grid = QGridLayout()

        self.grid.addWidget(self.label_show_speed, 0, 0)
        self.grid.addWidget(self.label_digits_in_minute, 0, 1)
        self.grid.addWidget(self.label_mistakes_count, 1, 0)
        self.grid.addWidget(self.label_mistakes_count_, 1, 1)
        self.grid.addWidget(self.label_current_time, 2, 0)
        self.grid.addWidget(self.label_show_time, 2, 1)

        self.setLayout(self.grid)

    @staticmethod
    def show_mistakes(data: dict, stoppers: dict[str, str]):
        """ Функция проверки ошибок. Для сравнения берутся строка из файла
        задания и строка переведенная с кода морзе"""
        if data.get('time')[0] * 60 + data.get('time')[1] == 0:
            return ""
        new_string = ""
        first_array: str = data.get("initial_text").split("   ")
        second_array: str = data.get("verifiable_text").split("   ")
        for item1, item2 in zip(first_array, second_array):
            for base_letter, input_letter in zip(item2, item1):
                if base_letter != input_letter:
                    new_string += "<span style='color: red; text-decoration: underline;'>{}</span>".format(
                        base_letter)
                else:
                    new_string += base_letter
            difference = abs(len(item1) - len(item2))
            if len(item1) < len(item2):
                string = "<span style='color: red; text-decoration: underline;'>{}</span>"
                new_string += ''.join(map(lambda x: string.format(x), item1[-difference:]))
            new_string += "   "

        print(f"Исходный массив: {first_array}")
        print(f"Проверочный массив: {second_array}")

        return new_string
