import unittest

from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QEvent
from pages.page_main import MainWindow  # Import your application class


class TestMorseCodeTrainer(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.trainer = MainWindow()

    def tearDown(self):
        self.trainer.close()
        self.app.quit()

    def test_w_key_press_duration(self):
        # Simulate pressing and releasing the W key for durations that should translate to dots and dashes
        durations = [100, 300]  # Durations in milliseconds
        expected_symbols = ['.', '-']
        for duration, expected_symbol in zip(durations, expected_symbols):
            self.trainer.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_W))
            self.trainer.processEvent(QEvent(QEvent.KeyRelease, self.app))
            self.assertEqual(self.trainer.printMorseCode(expected_symbol), expected_symbol)


if __name__ == '__main__':
    unittest.main()
