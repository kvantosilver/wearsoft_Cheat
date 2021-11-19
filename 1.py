import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

HEIGHT = 800
WIDTH = 1300

class Menu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.menubar = parent.menuBar()
        self.file = self.menubar.addMenu('&Опции')


        self.exitAction = QAction(QIcon('cross-exit.ico'), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(parent.close)

        self.file.addAction(self.exitAction)

    def addMenu(self, actionName, text, command, icon, shortcut=None, statusTip=None) :
        self.actionName = QAction(QIcon(icon), text, self)
        if shortcut:
            self.actionName.setShortcut(shortcut)
        if statusTip:
            self.actionName.setStatusTip(statusTip)
        self.actionName.triggered.connect(command)

        self.file.insertAction(self.exitAction, self.actionName)


class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.initUI()

    def initUI(self):
        self.q = QDesktopWidget().availableGeometry()
        self.r_w, self.r_h = self.q.width(), self.q.height()
        self.setGeometry(self.r_w/2-WIDTH/2, self.r_h/2-HEIGHT/2, WIDTH, HEIGHT)
        self.setFixedSize(1300, 800)
        self.setWindowTitle('Lings2')
        self.setWindowIcon(QIcon('Lings.ico'))
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.buttons = []
        for i in range(5):
            but = QtWidgets.QPushButton('button {}'.format(i), self)
            self.mainLayout.addWidget(but)
            self.buttons.append(but)
        self.setLayout(self.mainLayout)
        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.q = QDesktopWidget().availableGeometry()
        self.r_w, self.r_h = self.q.width(), self.q.height()
        self.setGeometry(self.r_w/2-WIDTH/2, self.r_h/2-HEIGHT/2, WIDTH, HEIGHT)
        self.setFixedSize(1300, 800)
        self.setWindowTitle('Lings')
        self.setWindowIcon(QIcon('Lings.ico'))
        self.menu = Menu(self)

#        self.menu.addMenu('action', 'New', lambda: SecondWindow(), 'test.ico', shortcut="Ctrl+D", statusTip="Creating")
        self.menu.addMenu('action', 'New', lambda: SecondWindow(self), 'test.ico', shortcut="Ctrl+D", statusTip="Creating")
        #                                                       ^^^^


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())