# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Programming/Python/GUI/RecordedFootage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

class Ui_recordedFootageMenu(object):
    def __init__(self):
        self.mode_selected = None
        self.video_selected = None
        self.folder_selected = None

    def setupUi(self, recordedFootageMenu):
        recordedFootageMenu.setObjectName("recordedFootageMenu")
        recordedFootageMenu.resize(600, 300)
        self.centralwidget = QtWidgets.QWidget(recordedFootageMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(150, 170, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, -10, 381, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.buttonLoadVideo = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLoadVideo.setGeometry(QtCore.QRect(360, 40, 75, 23))
        self.buttonLoadVideo.setObjectName("buttonLoadVideo")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 40, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 80, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.buttonLoadFolder = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLoadFolder.setGeometry(QtCore.QRect(360, 80, 75, 23))
        self.buttonLoadFolder.setObjectName("buttonLoadFolder")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(150, 230, 441, 16))
        self.label_4.setObjectName("label_4")
        self.labelThreshhold = QtWidgets.QLabel(self.centralwidget)
        self.labelThreshhold.setGeometry(QtCore.QRect(210, 120, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelThreshhold.setFont(font)
        self.labelThreshhold.setObjectName("labelThreshhold")
        self.labelThreshold2 = QtWidgets.QLabel(self.centralwidget)
        self.labelThreshold2.setGeometry(QtCore.QRect(210, 140, 271, 16))
        self.labelThreshold2.setObjectName("labelThreshold2")
        self.detectionThreshold = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.detectionThreshold.setGeometry(QtCore.QRect(360, 120, 71, 21))
        self.detectionThreshold.setDecimals(1)
        self.detectionThreshold.setMinimum(1.0)
        self.detectionThreshold.setProperty("value", 99.0)
        self.detectionThreshold.setObjectName("detectionThreshold")
        recordedFootageMenu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(recordedFootageMenu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        recordedFootageMenu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(recordedFootageMenu)
        self.statusbar.setObjectName("statusbar")
        recordedFootageMenu.setStatusBar(self.statusbar)

        self.retranslateUi(recordedFootageMenu)
        QtCore.QMetaObject.connectSlotsByName(recordedFootageMenu)

        self.pushButton.clicked.connect(self.finish)
        self.buttonLoadVideo.clicked.connect(self.openFile)
        self.buttonLoadFolder.clicked.connect(self.openFolder)

    def retranslateUi(self, recordedFootageMenu):
        _translate = QtCore.QCoreApplication.translate
        recordedFootageMenu.setWindowTitle(_translate("recordedFootageMenu", "Recorded Footage"))
        self.pushButton.setText(_translate("recordedFootageMenu", "Select Option ^"))
        self.label.setText(_translate("recordedFootageMenu", "Make sure video files are .mp4 format!"))
        self.buttonLoadVideo.setText(_translate("recordedFootageMenu", "Load Video"))
        self.label_2.setText(_translate("recordedFootageMenu", "Process a single video:"))
        self.label_3.setText(_translate("recordedFootageMenu", "Process entire folder of videos:"))
        self.buttonLoadFolder.setText(_translate("recordedFootageMenu", "Load Folder"))
        self.label_4.setText(_translate("recordedFootageMenu", ""))
        self.labelThreshhold.setText(_translate("recordedFootageMenu", "Confidence Threshold: "))
        self.labelThreshold2.setText(_translate("recordedFootageMenu", "Not reccomended to be below 90% when saving images"))
        self.detectionThreshold.setSuffix(_translate("recordedFootageMenu", "%"))

    def openFile(self):
        _translate = QtCore.QCoreApplication.translate
        file_data = QFileDialog.getOpenFileName(None, "Select a video", "", "Video Files (*.mp4)")
        filename = file_data[0]
        filetype = (file_data[0][-3:])

        # Extra Check
        if(filetype == "mp4" or filetype == "MP4"):
            self.mode_selected = "video"
            self.video_selected = filename
            self.pushButton.setEnabled(True)
            self.pushButton.setText(_translate("recordedFootageMenu", "Process Video"))
            self.label_4.setText(_translate("recordedFootageMenu", "File: " + self.video_selected))
        else:
            self.pushButton.setEnabled(False)
            self.mode_selected = None
            self.video_selected = None
            self.pushButton.setText(_translate("recordedFootageMenu", "Select Option ^"))
            self.label_4.setText(_translate("recordedFootageMenu", ""))

    def openFolder(self):
        _translate = QtCore.QCoreApplication.translate
        folder_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        if(folder_path != ""):
            self.mode_selected = "folder"
            self.folder_selected = folder_path
            self.pushButton.setEnabled(True)
            self.pushButton.setText(_translate("recordedFootageMenu", "Process Folder"))
            self.label_4.setText(_translate("recordedFootageMenu", "Folder: " + self.folder_selected))
        else:
            self.pushButton.setEnabled(False)
            self.mode_selected = None
            self.folder_selected = None
            self.pushButton.setText(_translate("recordedFootageMenu", "Select Option ^"))
            self.label_4.setText(_translate("recordedFootageMenu", ""))

    def finish(self):
        threshold = self.detectionThreshold.value() / 100

        if(self.mode_selected == "video"):
            print("./darknet detector demo cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights " + self.video_selected + " -save -thresh %3.2f" %(threshold))
        elif(self.mode_selected == "folder"):
            print("./darknet detector demo cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights / -save -folder " + self.folder_selected + " -thresh %3.2f" %(threshold))
        elif(self.mode_selected == None):
            print("An error occurred")
        else:
            print("If you see this then worry. Should never happen")

        exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    recordedFootageMenu = QtWidgets.QMainWindow()
    ui = Ui_recordedFootageMenu()
    ui.setupUi(recordedFootageMenu)
    recordedFootageMenu.show()
    sys.exit(app.exec_())
