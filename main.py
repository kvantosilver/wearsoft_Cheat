import pandas as pd
from datetime import date
import sys
from PyQt5 import uic
import mysql.connector
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QLineEdit,
    QFileDialog,
    QInputDialog,
    QMessageBox,
)
from PyQt5 import QtGui
from PyQt5.QtWidgets import QInputDialog, QTableWidgetItem
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
        uic.loadUi("design/load stress.ui", self)
        self.update_data_table()
        self.setWindowIcon(QtGui.QIcon("Resources/icon.png"))
        # Заполняем табл
        self.addStrees.clicked.connect(self.add_strees_in_db)
        self.connection.close()

    def add_strees_in_db(self):
        self.file = open("data/setting.txt", encoding="UTF-8")
        data = self.file.readlines()
        self.file.close()
        self.connection = mysql.connector.connect(
            host=data[0][:-1],
            user=data[1][:-1],
            password=data[2][:-1],
            database=data[3],
        )
        if self.stressData.text() != "":
            data = [
                self.stressData.text(),
                self.yeardata.text(),
                self.dataQuartal.text(),
                self.datapart.text(),
                self.dataWay.text(),
                str(date.today().strftime("%d:%B:%Y")),
            ]
            query = f"""INSERT INTO stress_table(stress_data, year, quarter, part, way, data) values("{data[0]}", "{data[1]}", "{data[2]}", "{data[3]}", "{data[4]}", "{data[5]}")"""
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            self.update_data_table()

    def update_data_table(self):
        self.file = open("data/setting.txt", encoding="UTF-8")
        data = self.file.readlines()
        self.file.close()
        self.connection = mysql.connector.connect(
            host=data[0][:-1],
            user=data[1][:-1],
            password=data[2][:-1],
            database=data[3],
        )

        query = """DESCRIBE stress_table"""
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(0)
        rows_table = []
        for element in result:
            rows_table.append(element[0])
            print(f"'{element[0]}'", end=" ")
        self.tableWidget.setHorizontalHeaderLabels(rows_table)
        print(result)
        query = """Select * From stress_table"""
        cursor.execute(query)
        result = cursor.fetchall()
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


class MainWearDesign(QMainWindow):
    def __init__(self):
        super().__init__()
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        uic.loadUi("design/Main.ui", self)
        self.setWindowIcon(QtGui.QIcon("Resources/icon.png"))
        self.update_table_widget()
        self.settingfile = ""
        self.actionSetting.triggered.connect(self.setting_open)
        self.actionOpenStress.triggered.connect(self.strees_open)
        self.actionImport.triggered.connect(self.import_xlxs)
        self.actionExport.triggered.connect(self.export_xlxs)

    def update_table_widget(self):
        self.file = open("data/setting.txt", encoding="UTF-8")
        data = self.file.readlines()
        self.file.close()
        self.connection = mysql.connector.connect(
            host=data[0][:-1],
            user=data[1][:-1],
            password=data[2][:-1],
            database=data[3],
        )

        query = """DESCRIBE resault_iznos"""
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query)
        result = cursor.fetchall()
        self.tableWidget.setColumnCount(17)
        self.tableWidget.setRowCount(0)
        rows_table = []
        for element in result:
            rows_table.append(element[0])
            print(f"'{element[0]}'", end=" ")
        self.tableWidget.setHorizontalHeaderLabels(rows_table)
        print(result)
        query = """Select * From resault_iznos"""
        cursor.execute(query)
        result = cursor.fetchall()
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.connection.close()

    def strees_open(self):
        self.settingfile = LoadStress()
        self.settingfile.show()

    def setting_open(self):
        self.settingfile = SettingMainR()
        self.settingfile.show()

    def import_xlxs(self):
        fname = QFileDialog.getOpenFileName(
            self, "Выбрать картинку", "", "Файл Excel (*.xlsx);;Все файлы (*)"
        )[0]
        year, ok_pressed = QInputDialog.getInt(
            self, "Год", "Введите год", 2021, 2000, 2099, 1
        )
        if ok_pressed:
            quarter, ok_pressed = QInputDialog.getItem(
                self, "Квартал", "Выберите Квартал", ("1", "2", "3", "4"), 1, False
            )
            if not ok_pressed:
                win = QMessageBox()
                win.setWindowTitle("Сообщение")
                win.setText("Ошибка импорта")
                win.exec()
                return ""
        else:
            win = QMessageBox()
            win.setWindowTitle("Сообщение")
            win.setText("Ошибка импорта")
            win.exec()
            return ""
        collection350 = (
            pd.read_excel(fname, sheet_name="до 350")
            .to_csv(index=False)
            .split("\r\n")[2:]
        )
        collection650 = (
            pd.read_excel(fname, sheet_name="351-650")
            .to_csv(index=False)
            .split("\r\n")[2:]
        )
        collection1200 = (
            pd.read_excel(fname, sheet_name="651-1200")
            .to_csv(index=False)
            .split("\r\n")[2:]
        )
        self.file = open("data/setting.txt", encoding="UTF-8")
        data = self.file.readlines()
        self.connection = mysql.connector.connect(
            host=data[0][:-1],
            user=data[1][:-1],
            password=data[2][:-1],
            database=data[3],
        )
        query = f'''Select stress_data From stress_table WHERE year = "{str(year)}" AND quarter = "{str(quarter)}"'''
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query)
        stress_data = cursor.fetchone()
        # ПРОВЕРКА НА ГРУЗ
        val_query = []
        for element in collection350:
            list_element = element.split(",")
            pin = []
            for index in range(len(list_element)):
                if index == 9:
                    pin.append(str(stress_data[0]))
                    pin.append(list_element[index])
                elif index == 12:
                    if list_element[11] != "":
                        pin.append(
                            str(
                                round(
                                    float(list_element[11]) / float(stress_data[0]), 5
                                )
                            )
                        )
                        pin.append(list_element[index])
                    else:
                        pin.append(
                            str(
                                round(
                                    float(list_element[12]) / float(stress_data[0]), 5
                                )
                            )
                        )
                        pin.append(list_element[index])
                else:
                    pin.append(list_element[index])
            val_query.append(tuple(pin))
        i = val_query.pop(-1)
        for element in collection650:
            list_element = element.split(",")
            pin = []
            for index in range(len(list_element)):
                if index == 9:
                    pin.append(str(stress_data[0]))
                    pin.append(list_element[index])
                elif index == 12:
                    if list_element[11] != "":
                        pin.append(
                            str(
                                round(
                                    float(list_element[11]) / float(stress_data[0]), 5
                                )
                            )
                        )
                        pin.append(list_element[index])
                    else:
                        pin.append(
                            str(
                                round(
                                    float(list_element[12]) / float(stress_data[0]), 5
                                )
                            )
                        )
                        pin.append(list_element[index])
                else:
                    pin.append(list_element[index])
            val_query.append(tuple(pin))
        i = val_query.pop(-1)
        for element in collection1200:
            list_element = element.split(",")
            pin = []
            for index in range(len(list_element)):
                if index == 9:
                    pin.append(str(stress_data[0]))
                    pin.append(list_element[index])
                elif index == 12:
                    if list_element[11] != "":
                        pin.append(
                            str(
                                round(
                                    float(list_element[11]) / float(stress_data[0]), 5
                                )
                            )
                        )
                        pin.append(list_element[index])
                    else:
                        pin.append(
                            str(
                                round(
                                    float(list_element[12]) / float(stress_data[0]), 5
                                )
                            )
                        )
                        pin.append(list_element[index])
                else:
                    pin.append(list_element[index])
            val_query.append(tuple(pin))
        i = val_query.pop(-1)
        query = f"""INSERT INTO `resault_iznos`(`ПЧ`, `Направление`, `Путь`, `Нач.крив Км`, `Нач.крив М`, `Длина кривой`, `Длина круговой`, `Длина переходн`, `R`, `Груз-нность`, `Пропущ. тоннаж`, `Скорость`, `Интенсивность БИ`, `РБИ мм/год`, `Износ средн`, `Износ макс`, `Дата последнего измерения`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        for element in val_query:
            cursor.execute(query, element)
            self.connection.commit()
        self.connection.close()
        self.file.close()
        self.update_table_widget()

    def export_xlxs(self):
        fname = QFileDialog.getSaveFileName(
            self, "Сохранить файл", ".xlsx", "All Files(*.*)"
        )
        win = QMessageBox()
        win.setWindowTitle("Сообщение")
        win.setText("Соединение установлено")
        win.exec()


def main():
    file = open("data/key", encoding="UTF-8")
    data = file.readline()
    if data == "'ghkjalf;uwqfup1up31u32u09407209hneklwf&*W)&W*e37921hio'":
        app = QApplication(sys.argv)
        ex = MainWearDesign()
        ex.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
