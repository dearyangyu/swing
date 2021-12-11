# -*- coding: utf-8 -*-

from PySide2.QtGui import QStandardItem, QStandardItemModel

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1

from wildchildanimation.gui.shot_list_dialog import Ui_ShotListDialog


'''
    List selected files
    ################################################################################
'''

class ShotListDialog(QtWidgets.QDialog, Ui_ShotListDialog):

    def __init__(self, parent = None, shot_list = []):
        super(ShotListDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("swing: select shots")
        self.shot_list = shot_list

        self.load()
        self.status = 'OK'

        self.buttonClear.clicked.connect(self.clear_items)
        self.buttonCancel.clicked.connect(self.cancel_dialog)
        self.buttonOk.clicked.connect(self.close_dialog)

    def load(self):
        model = QStandardItemModel()
        for item in self.shot_list:
            list_item = QStandardItem(item)

            list_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            list_item.setCheckable(True) 
            list_item.setCheckState(QtCore.Qt.Checked)

            model.appendRow(list_item)

        self.listView.setModel(model)

    def clear_items(self):
        self.shot_list = []
        self.load()

    def close_dialog(self):
        self.status = 'OK'
        self.close()

    def cancel_dialog(self):
        self.status = 'Cancel'
        self.close()                    

        


