# -*- coding: utf-8 -*-

import traceback
import sys
import os
import re
import copy
import requests

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    import sip
    qtMode = 1

from wildchildanimation.gui.entity_select_widget import Ui_EntitySelectWidget

'''
    EntitySelectDialog class
    ################################################################################
'''

class EntitySelectDialog(QtWidgets.QDialog, Ui_EntitySelectWidget):

    working_dir = None
    
    def __init__(self, parent = None, title = "Select Items"):
        super(EntitySelectDialog, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(title)

        self.pushButtonOK.clicked.connect(self.close_dialog)
        self.pushButtonCancel.clicked.connect(self.cancel)   

        self.toolButtonSelectAll.clicked.connect(self.select_all)
        self.toolButtonSelectNone.clicked.connect(self.select_none)

    def select_all(self):
        for row in range(self.listWidget.count()):
            self.listWidget.item(row).setCheckState(QtCore.Qt.Checked)
        self.listWidget.update()            

    def select_none(self):
        for row in range(self.listWidget.count()):
            self.listWidget.item(row).setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.update()

    def get_selection(self):
        selection = []

        for row in range(self.listWidget.count()):
            item = self.listWidget.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                data = item.data(QtCore.Qt.UserRole)
                selection.append(data)

        return selection

    def close_dialog(self):
        self.accept()
        self.close()

    def cancel(self):
        self.reject()
        self.close()

    def load(self, items, selection = None):
        for item in items:
            li = QtWidgets.QListWidgetItem()
            li.setText(item['name'])
            li.setData(QtCore.Qt.UserRole, item)
            li.setFlags(li.flags() | QtCore.Qt.ItemIsUserCheckable)

            if "color" in item:
                li.setForeground(QtGui.QColor(item["color"]))            

            if selection and item in selection:
                li.setCheckState(QtCore.Qt.Checked)
            else:
                li.setCheckState(QtCore.Qt.Unchecked)

            self.listWidget.addItem(li)

