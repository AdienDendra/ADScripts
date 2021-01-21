from __builtin__ import long
import pymel.core as pm
import maya.OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class ADCtrlDialog(QtWidgets.QDialog):
    dialogInstance = None

    @classmethod
    def display(cls):
        if not cls.dialogInstance:
            cls.dialogInstance = ADCtrlDialog()

        if cls.dialogInstance.isHidden():
            cls.dialogInstance.show()

        else:
            cls.dialogInstance.raise_()
            cls.dialogInstance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        super(ADCtrlDialog, self).__init__(parent)

        self.setWindowTitle("AD Controller")
        self.setMinimumWidth(350)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.initialColor = QtGui.QColor(255, 0, 0)

        self.create_widgets()
        self.create_layouts()

        self.create_connection()

    def create_widgets(self):
        self.line_prefix_name = QtWidgets.QLineEdit()
        # self.linePrefixName.setFixedWidth(200)
        self.check_box_prefix_name = QtWidgets.QCheckBox()
        self.line_suffix_name = QtWidgets.QLineEdit()
        # self.lineSuffixName.setFixedWidth(200)

        self.line_grp_ctrl = QtWidgets.QLineEdit()
        # self.lineGrpCtrl.setFixedWidth(200)

        self.spin_box_ctrl_size = QtWidgets.QDoubleSpinBox()
        self.spin_box_ctrl_size.setFixedWidth(80)
        self.spin_box_ctrl_size.setMaximum(100.00)
        self.spin_box_ctrl_size.setMinimum(0.01)
        self.spin_box_ctrl_size.setValue(1.00)

        self.obj_visibility = QtWidgets.QCheckBox()
        self.color_button = QtWidgets.QPushButton('Show Colors')

        # GIMBAL CTRL
        self.gimbal_ctrl = QtWidgets.QCheckBox()
        self.translate_gimbal_all = QtWidgets.QCheckBox('All')
        self.translate_gimbal_X = QtWidgets.QCheckBox('X')
        self.translate_gimbal_Y = QtWidgets.QCheckBox('Y')
        self.translate_gimbal_Z = QtWidgets.QCheckBox('Z')

        self.rotate_gimbal_all = QtWidgets.QCheckBox('All')
        self.rotate_gimbal_X = QtWidgets.QCheckBox('X')
        self.rotate_gimbal_Y = QtWidgets.QCheckBox('Y')
        self.rotate_gimbal_Z = QtWidgets.QCheckBox('Z')

        # self.checkBox1 = QtWidgets.QCheckBox("CheckBox1")
        # self.checkBox2 = QtWidgets.QCheckBox("Chec kBox2")
        # self.button1   = QtWidgets.QPushButton("Button 1")
        # self.button2   = QtWidgets.QPushButton("Button 2")

    def create_layouts(self):

        form_layout = QtWidgets.QFormLayout()
        # PREFIX LAYOUT
        prefix_name_layout = QtWidgets.QHBoxLayout()
        prefix_name_layout.addWidget(self.check_box_prefix_name)
        prefix_name_layout.addWidget(self.line_prefix_name)
        form_layout.addRow("Prefix Name:", prefix_name_layout)

        form_layout.addRow("Suffix Name:", self.line_suffix_name)
        form_layout.addRow("Group Parent Name:", self.line_grp_ctrl)
        form_layout.addRow("Controller Size:", self.spin_box_ctrl_size)
        form_layout.addRow("Object Hide:", self.obj_visibility)
        form_layout.addRow("Color Ctrl:", self.color_button)
        form_layout.addRow("Gimbal Ctrl:", self.gimbal_ctrl)
        form_layout.addRow("Translate:", self.translate_gimbal_all)
        form_layout.addRow("Rotate:", self.rotate_gimbal_all)

        translate_gimbal_layout = QtWidgets.QHBoxLayout()
        translate_gimbal_layout.addWidget(self.translate_gimbal_all)
        translate_gimbal_layout.addWidget(self.translate_gimbal_X)
        translate_gimbal_layout.addWidget(self.translate_gimbal_Y)
        translate_gimbal_layout.addWidget(self.translate_gimbal_Z)

        translate_gimbal_layout.addWidget(self.rotate_gimbal_all)
        translate_gimbal_layout.addWidget(self.rotate_gimbal_X)
        translate_gimbal_layout.addWidget(self.rotate_gimbal_Y)
        translate_gimbal_layout.addWidget(self.rotate_gimbal_Z)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(translate_gimbal_layout)

        # mainLayout.addLayout(rGimbalLayout)
        # mainLayout.addLayout(gimbalLayout)

    def create_connection(self):
        self.line_prefix_name.editingFinished.connect(self.line_prefix_name_text)
        self.line_suffix_name.editingFinished.connect(self.line_suffix_name_text)

        self.obj_visibility.toggled.connect(self.hidden_object_vis)
        self.gimbal_ctrl.toggled.connect(self.gimbal_ctrl_create)
        self.color_button.clicked.connect(self.color_selected_ctrl)

    def color_selected_ctrl(self):
        self.initialColor = QtWidgets.QColorDialog.getColor(self.initialColor, self)
        print("Red:{0} Green:{1} Blue:{2}".format(self.initialColor.red(),
                                                  self.initialColor.green(),
                                                  self.initialColor.blue()))

    def line_prefix_name_text(self):
        prefixName = self.line_prefix_name.text()
        print(prefixName)

    def line_suffix_name_text(self):
        suffixName = self.line_suffix_name.text()
        print('_%s' % suffixName)

    def hidden_object_vis(self):
        hidden = self.obj_visibility.isChecked()
        if hidden:
            print('Hidden')
        else:
            print('Visible')
        # mainLayout.addWidget(self.linePrefixName)
        # mainLayout.addWidget(self.checkBox1)
        # mainLayout.addWidget(self.checkBox2)
        # mainLayout.addWidget(self.button1)
        # mainLayout.addWidget(self.button2)

    def gimbal_ctrl_create(self):
        create = self.gimbal_ctrl.isChecked()
        if create:
            print('Create')
        else:
            print('Not Create')

# if __name__ == "__main__":
#
#     try:
#         dialog.close() # pylint: disable=E0601
#         dialog.deleteLater()
#     except:
#         pass
#
#     dialog = ADCtrlDialog()
#     dialog.show()
