from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import requests
from requests.exceptions import ConnectionError
from PyQt5 import QtGui


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 200)
        self.flag = True
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_2.addWidget(self.radioButton, 4, 1, 1, 1)
        self.lineNameDB = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNameDB.setObjectName("lineNameDB")
        self.gridLayout_2.addWidget(self.lineNameDB, 5, 0, 1, 2)
        self.linePassword = QtWidgets.QLineEdit(self.centralwidget)
        self.linePassword.setObjectName("linePassword")
        self.gridLayout_2.addWidget(self.linePassword, 4, 0, 1, 1)
        self.lineNameUser = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNameUser.setObjectName("lineNameUser")
        self.gridLayout_2.addWidget(self.lineNameUser, 0, 0, 1, 2)
        self.lineNameHost = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNameHost.setObjectName("lineNameHost")
        self.gridLayout_2.addWidget(self.lineNameHost, 1, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 1, 4, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ConnectProverka = QtWidgets.QPushButton(self.centralwidget)
        self.ConnectProverka.setObjectName("ConnectProverka")
        self.horizontalLayout.addWidget(self.ConnectProverka)
        self.SaveSetting = QtWidgets.QPushButton(self.centralwidget)
        self.SaveSetting.setObjectName("SaveSetting")
        self.horizontalLayout.addWidget(self.SaveSetting)
        self.SelectRepository = QtWidgets.QPushButton(self.centralwidget)
        self.SelectRepository.setObjectName("SelectRepository")
        self.horizontalLayout.addWidget(self.SelectRepository)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 2)
        # MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.file = open("data/setting.txt", encoding="UTF-8")
        data = self.file.readlines()
        self.lineNameUser.setText(f"{data[1][:-1]}")
        self.lineNameHost.setText(f"{data[0][:-1]}")
        self.linePassword.setText(f"{data[2][:-1]}")
        self.linePassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineNameDB.setText(f"{data[3]}")
        self.SaveSetting.clicked.connect(self.save_change)
        self.radioButton.toggled.connect(self.change_pass_status)
        self.ConnectProverka.clicked.connect(self.connect_mysql)
        MainWindow.setWindowTitle(_translate("MainWindow", "??????????????????"))
        self.label_3.setText(_translate("MainWindow", "?????? ????????????????????????"))
        self.radioButton.setText(_translate("MainWindow", "???????????????? ????????????"))
        self.label.setText(_translate("MainWindow", "?????? ??????????"))
        self.label_2.setText(_translate("MainWindow", "????????????"))
        self.label_4.setText(_translate("MainWindow", "?????? ????????"))
        self.ConnectProverka.setText(_translate("MainWindow", "???????????????? ????????????????????"))
        self.SaveSetting.setText(_translate("MainWindow", "?????????????????? ??????????????????"))
        self.SelectRepository.setText(_translate("MainWindow", "?????????? ??????????????????????"))

    def save_change(self):
        self.file = open("data/setting.txt", mode="w", encoding="UTF-8")
        print(self.lineNameHost.text(), file=self.file)
        print(self.lineNameUser.text(), file=self.file)
        print(self.linePassword.text(), file=self.file)
        print(self.lineNameDB.text(), file=self.file)
        self.file.close()

    def connect_mysql(self):
        print(self.linePassword.text())
        win = QtWidgets.QMessageBox()
        win.setWindowTitle("??????????????????")
        try:

            print(f"host={self.lineNameHost.text()}")
            print(f"user={self.lineNameUser.text()}")
            print(f"password={self.linePassword.text()}")
            print(f" database={self.lineNameDB.text()}")
            try:
                r = requests.get("http://192.168.1.50")
                r.raise_for_status()
                print("Internet connection detected.")
            except ConnectionError as e:
                print("Internet connection not detected.")
                raise e
            connection = mysql.connector.connect(
                host=self.lineNameHost.text(),
                user=self.lineNameUser.text(),
                password=self.linePassword.text(),
                database=self.lineNameDB.text(),
            )
            connection.close()
            win.setText("???????????????????? ??????????????????????")
            win.exec()
        except:
            win.setText("???????????????????? ???? ??????????????????????")
            win.exec()

    def change_pass_status(self):
        if self.flag:
            self.linePassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.linePassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.flag = not self.flag
