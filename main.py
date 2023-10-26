import sqlite3

from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("qt.ui", self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)

    def calendarDateChanged(self):
        pass

    def saveChanges(self):
        pass

    def addNewTask(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
