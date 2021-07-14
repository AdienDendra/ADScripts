import pymel.core as pm
class Test(object):
    def __init__(self):
        self.WINDOW_NAME = 'test'
        self.prevValue = 0
    def UI(self):
        with pm.window(self.WINDOW_NAME, widthHeight=(200, 200))  as self.mainWindow:
            with pm.rowColumnLayout(nc=1):
                self.slider = pm.floatSlider( w=500,min=-10, max=10, value=0, step=0.0001, changeCommand=pm.Callback(self.action) , dragCommand=pm.Callback(self.dragSlider))
    def action(self):
        print('action')
        pm.floatSlider(self.slider, edit=True, v=0)
        self.prevValue = 0
    def dragSlider(self):
        value = pm.floatSlider(self.slider, q=True, v=True)
        deltaValue = (value - self.prevValue)
        self.scaleAction( deltaValue )
        self.prevValue = value

    def scaleAction(self, deltaValue):
        objList = [pm.PyNode(node) for node in pm.ls(selection=True)]
        for obj in objList:
            currentScale = obj.scaleX.get()
            obj.scale.set([currentScale+deltaValue, currentScale+deltaValue,currentScale+deltaValue])
            pm.makeIdentity(apply=True, s=1, n=0)
main = Test()
main.UI()


##############################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import shiboken2
import maya.cmds as cmds
import maya.OpenMayaUI as mui


# Converted from UI file to python
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(201, 96)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)
        self.spinBox.setValue(100)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_2 = QSpinBox(self.centralwidget)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setValue(15)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_2.addWidget(self.spinBox_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.spinBox_3 = QSpinBox(self.centralwidget)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(100)
        self.spinBox_3.setValue(80)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_3.addWidget(self.spinBox_3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None))
        self.label.setText(QApplication.translate("MainWindow", "Tempruture :", None))
        self.label_2.setText(QApplication.translate("MainWindow", "Pressure :", None))
        self.label_3.setText(QApplication.translate("MainWindow", "Speed :", None))


def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QWidget)


class Form1Class(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=maya_main_window()):
        super(Form1Class, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    win = Form1Class()
    win.show()


###########################################################################################

import maya.cmds as cmds

rsWin = cmds.window()
rsForm = cmds.formLayout(numberOfDivisions=100)
rsText = cmds.text(label='Number : ')
rsTxtFld = cmds.intField(v=90)
rsClmLyt = cmds.columnLayout()
rsBut1 = cmds.button(label='x', h=10, w=10, c='rsIncTxtFld()')
rsBut2 = cmds.button(label='x', h=10, w=10, c='rsDecTxtFld()')
cmds.formLayout(rsForm, edit=True,
                attachForm=[(rsText, 'top', 8), (rsText, 'left', 5), (rsTxtFld, 'top', 5), (rsTxtFld, 'left', 55),
                            (rsClmLyt, 'top', 4), (rsClmLyt, 'left', 90)])
cmds.showWindow(rsWin)


def rsIncTxtFld():
    rsGetTxtFld = cmds.intField(rsTxtFld, q=1, v=90)
    cmds.intField(rsTxtFld, e=1, v=(rsGetTxtFld + 5))


def rsDecTxtFld():
    rsGetTxtFld = cmds.intField(rsTxtFld, q=1, v=90)
    cmds.intField(rsTxtFld, e=1, v=(rsGetTxtFld - 5))

