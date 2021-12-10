# -*- coding: utf-8 -*-

import traceback
import sys
import os
import copy
from PySide2.QtGui import QStandardItem, QStandardItemModel
import gazu

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1

from wildchildanimation.gui.file_list_dialog import Ui_fileListDialog


'''
    List selected files
    ################################################################################
'''

class FileListDialog(QtWidgets.QDialog, Ui_fileListDialog):

    def __init__(self, parent = None, file_list = []):
        super(FileListDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.file_list = file_list

        self.load()
        self.status = 'OK'

        self.buttonClear.clicked.connect(self.clear_items)
        self.buttonCancel.clicked.connect(self.cancel_dialog)
        self.buttonOk.clicked.connect(self.close_dialog)

    def load(self):
        model = QStandardItemModel()
        for item in self.file_list:
            file_item = QStandardItem(item)
            model.appendRow(file_item)
        self.listView.setModel(model)

    def clear_items(self):
        self.file_list = []
        self.load()

    def close_dialog(self):
        self.status = 'OK'
        self.close()

    def cancel_dialog(self):
        self.status = 'Cance;'
        self.close()                    

        


