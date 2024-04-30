import os

from PySide2.QtWidgets import (QWidget,
                               QLineEdit,
                               QFileDialog,
                               QComboBox, QGridLayout, QSizePolicy)

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

        self.label_group_amount = create_label(
            self,
            text="Количество групп",
            font_size=10
        )
        self.label_group_amount.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.text_field_group = QLineEdit(self)
        self.text_field_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.label_text_format = create_label(
            self,
            text="Формат текста",
            font_size=10
        )
        self.label_text_format.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("цифровой")
        self.combo_box.addItem("буквенный")
        self.combo_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.text_field = create_textfield(
            self,
        )
        self.save_button = create_button(
            self,
            name="Сохранить",
            func=self.save_text_to_file
        )
        self.generate_button = create_button(
            self,
            name="Сгенерировать",
            func=lambda: generate_random_string(
                self,
                self.text_field_group.text(),
                self.combo_box.currentText()
            )
        )

        # создадим лэйаут
        self.grid = QGridLayout()

        self.grid.addWidget(self.label_group_amount, 0, 0)
        self.grid.addWidget(self.text_field_group, 0, 1)
        self.grid.addWidget(self.label_text_format, 0, 2)
        self.grid.addWidget(self.combo_box, 0, 3)

        self.grid.addWidget(self.text_field, 1, 0, 1, 4)

        self.grid.addWidget(self.generate_button, 2, 0, 1, 2)
        self.grid.addWidget(self.save_button, 2, 2, 1, 2)

        # self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 3)
        self.grid.setRowStretch(2, 1)

        self.grid.setColumnMinimumWidth(0, 50)
        self.grid.setColumnMinimumWidth(1, 50)
        self.grid.setColumnMinimumWidth(2, 50)
        self.grid.setColumnMinimumWidth(3, 50)

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)
        self.grid.setColumnStretch(2, 1)
        self.grid.setColumnStretch(3, 1)

        self.setLayout(self.grid)

    def save_text_to_file(self):
        text = self.text_field.toPlainText()
        # Get the directory of the current script
        current_script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        filename = QFileDialog.getSaveFileName(
            self,
            "Save file",
            current_script_dir
        )
        if filename[0]:
            with open(filename[0], 'w') as f:
                f.write(text)
