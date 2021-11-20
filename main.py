import pandas as pd
import sys
from PyQt5 import uic
import pymysql
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLineEdit, QFileDialog, QInputDialog, QMessageBox
from PyQt5.QtWidgets import QInputDialog
from design.main_design import Ui_MainWindow as MainDesignPy
from design.setting import Ui_MainWindow as SettingDesign


class SettingMainR(QWidget, SettingDesign):
    def __init__(self):
        super().__init__()
        self.ui = SettingDesign()
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.ui.setupUi(self)


class LoadStress(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design/load stress.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run)
        # Обратите внимание: имя элемента такое же как в QTDesigner

    def run(self):
        self.label.setText("OK")
        # Имя элемента совпадает с objectName в QTDesigner


class MainWearDesign(QWidget, MainDesignPy):
    def __init__(self):
        super().__init__()
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.setupUi(self)
        self.settingfile = ''
        self.actionSetting.triggered.connect(self.setting_open)
        self.actionOpenStress.triggered.connect(self.strees_open)
        self.actionImport.triggered.connect(self.import_xlxs)
        self.actionExport.triggered.connect(self.export_xlxs)

    def strees_open(self):
        self.settingfile = LoadStress()
        self.settingfile.show()

    def setting_open(self):
        self.settingfile = SettingMainR()
        self.settingfile.show()

    def import_xlxs(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Файл Excel (*.xlsx);;Все файлы (*)')[0]
        year, ok_pressed = QInputDialog.getInt(self, "Год",
                                                "Введите год", 2021, 2000, 2099, 1)
        if ok_pressed:
            year, ok_pressed = QInputDialog.getItem(self, "Квартал",
                                                    "Выберите Квартал", ('1', '2', '3', '4'), 1, False)
            if not ok_pressed:
                win = QMessageBox()
                win.setWindowTitle('Сообщение')
                win.setText("Ошибка импорта")
                win.exec()
        else:
            win = QMessageBox()
            win.setWindowTitle('Сообщение')
            win.setText("Ошибка импорта")
            win.exec()
        print(fname)

    def export_xlxs(self):
        fname = QFileDialog.getSaveFileName(self,
                             "Сохранить файл",
                             ".xlsx",
                             "All Files(*.*)")
        print()

def main():
    app = QApplication(sys.argv)
    ex = MainWearDesign()
    ex.show()
    sys.exit(app.exec_())



main()