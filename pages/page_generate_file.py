import os

from PySide2.QtWidgets import (QWidget,
                               QLineEdit,
                               QFileDialog,
                               QComboBox)

from utils import (create_label,
                   create_textfield,
                   create_button,
                   generate_random_string)

STRING_TOTAL_LENGTH_IN_TEXT_EDIT = 599  # 100 групп * 5 символов + максимум


# 99 пробелов


class GeneratePageWindow(QWidget):
    """Класс для создания формы генерации шаблона задания """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генерация файла")
        self.setFixedSize(400, 290)

        self.label_group_amount = create_label(
            self,
            text="Количество групп",
            x=10,
            y=10,
            font_size=10
        )

        self.text_field_group = QLineEdit(self)
        self.text_field_group.move(130, 10)
        self.text_field_group.setFixedSize(40, 20)

        self.label_text_format = create_label(
            self,
            text="Формат текста",
            x=180,
            y=10,
            font_size=10
        )

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("цифровой")
        self.combo_box.addItem("буквенный")
        self.combo_box.move(270, 10)

        self.text_field = create_textfield(
            self,
            x=10,
            y=50,
            length=380,
            width=200,
        )
        self.save_button = create_button(
            self,
            name="Сохранить",
            x=250,
            y=255,
            func=self.save_text_to_file
        )
        self.generate_button = create_button(
            self,
            name="Сгенерировать",
            x=70,
            y=255,
            func=lambda: generate_random_string(
                self,
                self.text_field_group.text(),
                self.combo_box.currentText()
            )
        )

    def save_text_to_file(self):
        text = self.text_field.toPlainText()
        filename = QFileDialog.getSaveFileName(
            self,
            "Save file",
            os.path.expanduser("~/Desktop")
        )
        if filename[0]:
            with open(filename[0], 'w') as f:
                f.write(text)
