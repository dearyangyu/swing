# -*- coding: utf-8 -*-

import traceback
import sys
import os
import re

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance 
    import PySide2.QtUiTools as QtUiTools
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    import sip
    qtMode = 1

from wildchildanimation.gui.upload_monitor_dialog import Ui_UploadMonitorDialog    

'''
    UploadListModel class
    ################################################################################
'''

class UploadListModel(QtCore.QAbstractListModel):

    def __init__(self, parent, files = None):
        super(UploadListModel, self).__init__(parent)
        self.files = files or []
        self.status = {}

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the data structure.
            item = self.files[index.row()]
            text = self.status[item]

            # Return the todo text only.
            return "{} {}".format(item, text)

    def rowCount(self, index):
        return len(self.files)   

    def add_item(self, item, text):
        self.files.append(item)
        self.status[item] = text
        self.layoutChanged.emit()

    def set_item_text(self, item, text):
        self.status[item] = text
        self.layoutChanged.emit()

'''
    UploadMonitorDialog class
    ################################################################################
'''


class UploadMonitorDialog(QtWidgets.QDialog, Ui_UploadMonitorDialog):

    def __init__(self, parent = None, task = None):
        super(UploadMonitorDialog, self).__init__(parent) # Call the inherited classes __init__ method    
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(640)

        self.model = UploadListModel(self.listView)
        self.listView.setModel(self.model)
        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.task = task

        self.progressBar.setRange(0, len(self.model.files))

    def close_dialog(self):
        self.hide()

    def file_loading(self, status):
        message = status["message"]
        source = status["source"]     

        self.model.set_item_text(source, message)

    def file_loaded(self, status):
        print("file_loaded completed {0} files".format(self.progressBar.value()))

        message = status["message"]
        source = status["source"]     

        self.model.set_item_text(source, message)        
        self.progressBar.setValue(self.progressBar.value() + 1)

        if self.progressBar.value() >= len(self.model.files):
            QtWidgets.QMessageBox.question(self, 'Publishing complete', 'All files uploaded, thank you', QtWidgets.QMessageBox.Ok)
            try:
                url = gazu.task.get_task_url(self.task)
                self.open_url(url)
            except:
                print("Error loading url {0}".format(url))
                pass

    def add_item(self, source, text):
        self.model.add_item(source, text)         

    def reset_progressbar(self):
        self.progressBar.setRange(0, len(self.model.files))      
        self.progressBar.setValue(1)
        print("Upload monitor created for {0} files".format(len(self.model.files)))    

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')           
