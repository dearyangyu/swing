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
        self.setWindowTitle("swing: select files")

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.file_list = file_list

        self.load()
        self.status = 'OK'

        self.buttonClear.clicked.connect(self.select_none)
        #self.buttonAll.clicked.connect(self.select_all)
        self.buttonCancel.clicked.connect(self.cancel_dialog)
        self.buttonOk.clicked.connect(self.close_dialog)

    def load(self):
        self.model = QStandardItemModel()
        for item in self.file_list:
            list_item = QStandardItem(item)

            list_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            list_item.setCheckable(True) 
            list_item.setCheckState(QtCore.Qt.Checked)

            self.model.appendRow(list_item)

        self.listView.setModel(self.model)


    def is_all_selected(self):
        all_selected = True
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            all_selected = all_selected and item.checkState() == QtCore.Qt.Checked
        return all_selected

    def select_none(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)

    def select_all(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Checked)            

    def get_selected(self):
        selected = []
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                selected.append(item.text())
        return selected

    def close_dialog(self):
        self.status = 'OK'
        self.close()

    def cancel_dialog(self):
        self.status = 'Cancel'
        self.close()                    

        


