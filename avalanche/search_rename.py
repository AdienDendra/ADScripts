# from __builtin__ import long
import pymel.core as pm
import maya.OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class SearchRenameDialog(QtWidgets.QDialog):
    dialogInstance = None

    @classmethod
    def show_ui(cls):
        if not cls.dialogInstance:
            cls.dialogInstance = SearchRenameDialog()

        if cls.dialogInstance.isHidden():
            cls.dialogInstance.show()

        else:
            cls.dialogInstance.raise_()
            cls.dialogInstance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        super(SearchRenameDialog, self).__init__(parent)

        self.setWindowTitle("Search and Rename")
        self.setMinimumWidth(350)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        # self.initialColor = QtGui.QColor(255, 0, 0)

        self.create_widgets()
        self.create_layouts()
        self.create_connection()

    def create_widgets(self):
        self.line_find_name = QtWidgets.QLineEdit()
        self.line_find_name.setPlaceholderText('Find')

        self.line_rename_name = QtWidgets.QLineEdit()
        self.line_rename_name.setPlaceholderText('Rename')

        self.excute_button = QtWidgets.QPushButton('Do It')

    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()

        # LAYOUT
        prefix_name_layout = QtWidgets.QHBoxLayout()
        prefix_name_layout.addWidget(self.line_find_name)
        prefix_name_layout.addWidget(self.line_rename_name)
        prefix_name_layout.addWidget(self.excute_button)
        form_layout.addRow(prefix_name_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)

    def create_connection(self):
        self.line_find_name.editingFinished.connect(self.line_search_name_text)
        self.line_rename_name.editingFinished.connect(self.line_replace_name_text)
        self.excute_button.clicked.connect(self.excuted_renaming_name)

    def excuted_renaming_name(self):
        get_search_object = self.line_search_name_text()
        replacing_object = self.line_replace_name_text()

        if pm.objExists(get_search_object):
            try:
                pm.ls(replacing_object)
                replacing = get_search_object.replace(get_search_object, replacing_object)
                pm.rename(get_search_object, replacing)
            except Exception:
                pm.displayWarning('Replacing text is empty, skip replacing!')
        else:
            pm.displayError('There is no object %s exists in the scene' % get_search_object)

    def line_search_name_text(self):
        search = self.line_find_name.text()
        return search

    def line_replace_name_text(self):
        replace = self.line_rename_name.text()
        return replace

# from avalanche import search_rename
# reload(search_rename)
#
# SearchRenameDialog.show_ui()

# if __name__ == "__main__":
#
#     try:
#         dialog.close() # pylint: disable=E0601
#         dialog.deleteLater()
#     except:
#         pass
#
#     dialog = SearchRenameDialog()
#     dialog.show()
