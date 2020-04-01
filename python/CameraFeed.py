# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Programming/Python/GUI/CameraFeed.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import math


class Ui_cameraFeedMenu(object):
    def setupUi(self, cameraFeedMenu):
        cameraFeedMenu.setObjectName("cameraFeedMenu")
        cameraFeedMenu.resize(600, 300)
        self.centralwidget = QtWidgets.QWidget(cameraFeedMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.labelMain = QtWidgets.QLabel(self.centralwidget)
        self.labelMain.setGeometry(QtCore.QRect(80, -10, 481, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelMain.setFont(font)
        self.labelMain.setObjectName("labelMain")
        self.detectionThreshold = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.detectionThreshold.setGeometry(QtCore.QRect(180, 90, 71, 21))
        self.detectionThreshold.setDecimals(1)
        self.detectionThreshold.setMinimum(1.0)
        self.detectionThreshold.setMaximum(99.9)
        self.detectionThreshold.setProperty("value", 99.0)
        self.detectionThreshold.setObjectName("detectionThreshold")
        self.labelThreshhold = QtWidgets.QLabel(self.centralwidget)
        self.labelThreshhold.setGeometry(QtCore.QRect(30, 90, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelThreshhold.setFont(font)
        self.labelThreshhold.setObjectName("labelThreshhold")
        self.labelThreshold2 = QtWidgets.QLabel(self.centralwidget)
        self.labelThreshold2.setGeometry(QtCore.QRect(30, 110, 271, 16))
        self.labelThreshold2.setObjectName("labelThreshold2")
        self.screenCaptureToggle = QtWidgets.QCheckBox(self.centralwidget)
        self.screenCaptureToggle.setGeometry(QtCore.QRect(330, 90, 171, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.screenCaptureToggle.setFont(font)
        self.screenCaptureToggle.setObjectName("screenCaptureToggle")
        self.labelScreenCapture = QtWidgets.QLabel(self.centralwidget)
        self.labelScreenCapture.setGeometry(QtCore.QRect(330, 110, 271, 16))
        self.labelScreenCapture.setObjectName("labelScreenCapture")
        self.buttonMain = QtWidgets.QPushButton(self.centralwidget)
        self.buttonMain.setGeometry(QtCore.QRect(150, 170, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.buttonMain.setFont(font)
        self.buttonMain.setObjectName("buttonMain")
        cameraFeedMenu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(cameraFeedMenu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        cameraFeedMenu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(cameraFeedMenu)
        self.statusbar.setObjectName("statusbar")
        cameraFeedMenu.setStatusBar(self.statusbar)

        self.retranslateUi(cameraFeedMenu)
        QtCore.QMetaObject.connectSlotsByName(cameraFeedMenu)

        self.buttonMain.clicked.connect(self.startButton)

    def retranslateUi(self, cameraFeedMenu):
        _translate = QtCore.QCoreApplication.translate
        cameraFeedMenu.setWindowTitle(_translate("cameraFeedMenu", "Camera Feed"))
        self.labelMain.setText(_translate("cameraFeedMenu", "Make sure you have a camera installed before running!"))
        self.detectionThreshold.setSuffix(_translate("cameraFeedMenu", "%"))
        self.labelThreshhold.setText(_translate("cameraFeedMenu", "Confidence Threshold: "))
        self.labelThreshold2.setText(_translate("cameraFeedMenu", "Not reccomended to be below 90% when saving images"))
        self.screenCaptureToggle.setText(_translate("cameraFeedMenu", "Save Screencaptures?"))
        self.labelScreenCapture.setText(_translate("cameraFeedMenu", "Screencaptures will be saved to \"src/screenshots\""))
        self.buttonMain.setText(_translate("cameraFeedMenu", "START"))

    def startButton(self):
        enableScreenCapture = self.screenCaptureToggle.isChecked()
        threshold = self.detectionThreshold.value() / 100
        if(not enableScreenCapture):
            print("./darknet detector demo cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights -thresh %3.2f" %(threshold))
        else:
            print("./darknet detector demo cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights / -save -thresh %3.2f" %(threshold))

        exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    cameraFeedMenu = QtWidgets.QMainWindow()
    ui = Ui_cameraFeedMenu()
    ui.setupUi(cameraFeedMenu)
    cameraFeedMenu.show()
    sys.exit(app.exec_())
