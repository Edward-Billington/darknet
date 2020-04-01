# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Programming/Python/GUI/Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from CameraFeed import Ui_cameraFeedMenu
from RecordedFootage import Ui_recordedFootageMenu

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 10, 541, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.buttonCameraFeed = QtWidgets.QPushButton(self.centralwidget)
        self.buttonCameraFeed.setGeometry(QtCore.QRect(250, 160, 291, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.buttonCameraFeed.setFont(font)
        self.buttonCameraFeed.setObjectName("buttonCameraFeed")
        self.buttonPreRecorded = QtWidgets.QPushButton(self.centralwidget)
        self.buttonPreRecorded.setGeometry(QtCore.QRect(250, 310, 291, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.buttonPreRecorded.setFont(font)
        self.buttonPreRecorded.setObjectName("buttonPreRecorded")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # When the "Use Camera Feed" button is clicked
        self.buttonCameraFeed.clicked.connect(self.showCameraFeedMenu)
        self.buttonPreRecorded.clicked.connect(self.showPreRecordedMenu)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Knife Detector"))
        self.label.setText(_translate("MainWindow", "Welcome to the Weapon Detection GUI"))
        self.buttonCameraFeed.setText(_translate("MainWindow", "Use Camera Feed"))
        self.buttonPreRecorded.setText(_translate("MainWindow", "Use Recorded Footage"))

    def showCameraFeedMenu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_cameraFeedMenu()
        self.ui.setupUi(self.window)
        self.window.show()
        
    def showPreRecordedMenu(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_recordedFootageMenu()
        self.ui.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
