import pandas as pd
import sys
import pymysql
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLineEdit
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


class MainWearDesign(QWidget, MainDesignPy):
    def __init__(self):
        super().__init__()
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.setupUi(self)
        self.actionSetting.triggered.connect(self.setting_open)

    def setting_open(self):
        self.settingfile = SettingMainR()
        self.settingfile.show()

class Wear:
    def __init__(self, name_file):
        self.name_file = name_file
        self.data = ''

    def read_xlsx(self):
        collection = pd.read_excel(self.name_file, sheet_name=None)

        combined = pd.concat([value.assign(sheet_source=key)
                              for key, value in collection.items()],
                             ignore_index=True)
        pass

    def connect_mysql(self):
        con = pymysql.connect('localhost', 'user17',
                              's$cret', 'mydb')
        with con:
            cur = con.cursor()
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()
            print("Database version: {}".format(version[0]))

    def calculate_wear(self):
        pass


def main():
    w = Wear('Resources/РЦДМ износ.xlsx')
    w.read_xlsx()
    app = QApplication(sys.argv)
    ex = MainWearDesign()
    ex.show()
    sys.exit(app.exec_())



main()