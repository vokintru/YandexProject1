# Импорт библеотек
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import os


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)  # Подключение дизайна
        # Подключения
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)

    def setupUi(self, Form):  # Дизайн
        Form.setObjectName("Form")
        Form.resize(852, 426)
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        self.calendarWidget.setGeometry(QtCore.QRect(40, 60, 411, 311))
        self.calendarWidget.setStyleSheet("font:12pt;")
        self.calendarWidget.setObjectName("calendarWidget")
        self.tasksListWidget = QtWidgets.QListWidget(Form)
        self.tasksListWidget.setGeometry(QtCore.QRect(480, 60, 341, 301))
        self.tasksListWidget.setStyleSheet("font:12pt;")
        self.tasksListWidget.setObjectName("tasksListWidget")
        self.saveButton = QtWidgets.QPushButton(Form)
        self.saveButton.setGeometry(QtCore.QRect(480, 370, 341, 28))
        self.saveButton.setStyleSheet("")
        self.saveButton.setObjectName("saveButton")
        self.addButton = QtWidgets.QPushButton(Form)
        self.addButton.setGeometry(QtCore.QRect(730, 20, 93, 28))
        self.addButton.setStyleSheet("")
        self.addButton.setObjectName("addButton")
        self.taskLineEdit = QtWidgets.QLineEdit(Form)
        self.taskLineEdit.setGeometry(QtCore.QRect(480, 20, 241, 31))
        self.taskLineEdit.setStyleSheet("font:12pt;")
        self.taskLineEdit.setObjectName("taskLineEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):  # Дизайн
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.saveButton.setText(_translate("Form", "Save Changes"))
        self.addButton.setText(_translate("Form", "Add new"))

    def calendarDateChanged(self):  # Отслеживает изменения даты
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):  # Запись в базу данных
        # Подключаемся к базе
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        self.tasksListWidget.clear()  # Отчистка списка задач

        # Делаем запрос и обрабатываем его
        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:  # Добавление задач в список
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            self.tasksListWidget.addItem(item)

    def saveChanges(self):  # Сохранение отметок
        # Подключаемся к базе
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()  # Дата для сохранения

        for i in range(self.tasksListWidget.count()):  # Запись в БД
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()  # Сохранение изменений в БД

        messageBox = QMessageBox()
        messageBox.setText("Сохранено.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNewTask(self):  # Добавление новой задачи
        # Подключаемся к базе
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        # Сохраняем задачу и дату
        newTask = str(self.taskLineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()

        # Создаём запрос
        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "NO", date,)

        # Сорханяем
        cursor.execute(query, row)
        db.commit()

        # Выводим изменения
        self.updateTaskList(date)
        self.taskLineEdit.clear()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    if not os.path.isfile("data.db"):
        os.system(f"msg * Не найдена БД! Скачайте её отсюда: https://github.com/vokintru/YandexProject1")
    app = QApplication(sys.argv)
    window = Window()
    sys.excepthook = except_hook
    window.show()
    sys.exit(app.exec())
