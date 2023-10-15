import sys
import io
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QTableWidgetItem


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('qt.ui', self)  # Загружаем дизайн
        self.btnOpen.clicked.connect(self.open)
        self.btnSave.clicked.connect(self.save)
        self.file = "temp"
        self.f = open(self.file, "w")

    def open(self):
        try:
            self.file = QFileDialog.getOpenFileName(self, 'Выбрать файл', '',
                                                    'Текстовый файл (*.txt);;')[0]
            self.f = open(self.file, "r+")
            self.textEdit.setPlainText(self.f.read())
        except UnicodeDecodeError:
            self.status.setText("Ошибка декодирования (UnicodeDecodeError)")
        except Exception:
            self.status.setText("Неизвестная ошибка")

    def save(self):
        if self.file != "temp":
            self.f.close()
            self.f = open(self.file, "w")
            self.f.write(self.textEdit.toPlainText())
            self.f.close()
            self.f = open(self.file, "r+")
            self.textEdit.setPlainText(self.f.read())
        else:
            self.file = QFileDialog.getOpenFileName(self, 'Выбрать файл', '',
                                                    'Текстовый файл (*.txt);;')[0]
            self.f.close()
            self.f = open(self.file, "w")
            self.f.write(self.textEdit.toPlainText())
            self.f.close()
            self.f = open(self.file, "r+")
            self.textEdit.setPlainText(self.f.read())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
