from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QLabel


def return_mistakes_count(data: dict):
    """ Функция проверки ошибок. Для сравнения берутся строка из файла
    задания и строка переведенная с кода морзе"""
    count = 0
    for item1, item2 in zip(data["initial_text"],
                            data["verifiable_text"]):
        if item1 == item2:
            continue
        count += 1
    return count


def return_speed_printing(data: dict):
    """ Функция расчета времени печати по формуле
    длинна передаваемой строки / время с начала запуска """
    length = len(data['verifiable_text'])
    time_in_seconds = data['time'][0] * 60 + data['time'][1]
    print(f"Length: {length}")
    return round(length / time_in_seconds, 2)


class ResultWindow(QWidget):
    """ Класс для """
    def __init__(self, data: dict):
        super().__init__()
        self.setWindowTitle("Ваш результат")
        self.setFixedSize(350, 170)
        # ----------------------------------------------------------------

        # Графическая метка отображения скорости печати
        self.label_current_time = QLabel("Скорость - ", self)
        self.label_current_time.move(10, 10)
        self.label_current_time.setFont(QFont('Arial', 20))

        self.label_show_time = QLabel(f"{return_speed_printing(data)} зн/мин",
                                      self)
        self.label_show_time.move(200, 10)
        self.label_show_time.setFont(QFont('Arial', 20))
        #  ----------------------------------------------------------------
        # Графическая метка отображения полученных ошибок
        self.label_current_time = QLabel("Кол. ошибок - ", self)
        self.label_current_time.move(10, 50)
        self.label_current_time.setFont(QFont('Arial', 20))

        self.label_show_time = QLabel(f"{return_mistakes_count(data)}",
                                      self)
        self.label_show_time.move(200, 50)
        self.label_show_time.setFont(QFont('Arial', 20))

        # ----------------------------------------------------------------
        # Графическая метка отображения времени
        self.label_current_time = QLabel("Время - ", self)
        self.label_current_time.move(10, 100)
        self.label_current_time.setFont(QFont('Arial', 20))

        self.label_show_time = QLabel("00:00", self)
        self.label_show_time.move(200, 100)
        self.label_show_time.setFont(QFont('Arial', 20))
        minutes, seconds = divmod(data["time"][1], 60)
        self.label_show_time.setText(f"{minutes:02d}:{seconds:02d}")
