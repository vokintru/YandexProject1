import sys
import io
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QTableWidgetItem


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file = ""
        uic.loadUi('qt.ui', self)  # Загружаем дизайн
        self.btnOpen.clicked.connect(self.open)
        self.btnSave.clicked.connect(self.save)

    def open(self):
        self.file = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        print(self.file)

    def save(self):
        print('Clicked "Save"')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
