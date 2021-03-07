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

from datetime import datetime

import wildchildanimation.background_workers as bg

from wildchildanimation.gui.references_dialog import Ui_ReferencesDialog

from wildchildanimation.gui.swing_tables import human_size


class ReferencesDialogGUI(QtWidgets.QDialog, Ui_ReferencesDialog):

    working_dir = None
    
    def __init__(self, parent = None, handler = None, entity = None):
        super(ReferencesDialogGUI, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(500)

        self.handler = handler
        self.entity = entity

        if self.handler:
            self.files = self.handler.list_unresolved()
        else:
            self.files = []

        self.threadpool = QtCore.QThreadPool.globalInstance()

        loader = bg.EntityLoaderThread(self, self.entity["id"])
        loader.callback.loaded.connect(self.entity_loaded)
        self.threadpool.start(loader)        

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        self.toolButtonWeb.setEnabled(False)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)               

        #self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        load_table_widget(self.tableWidget, self.files)

        self.toolButtonAll.clicked.connect(self.select_all)
        self.toolButtonNone.clicked.connect(self.select_none)

        self.setWorkingDir(load_settings("projects_root", os.path.expanduser("~")))

    def select_all(self):
        index = 0
        while index < self.tableWidget.rowCount():
            row_item = self.tableWidget.item(index, 0)
            row_item.setCheckState(QtCore.Qt.Checked)
            index += 1

    def select_none(self):
        index = 0
        while index < self.tableWidget.rowCount():
            row_item = self.tableWidget.item(index, 0)
            row_item.setCheckState(QtCore.Qt.Unchecked)
            index += 1

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')        

    def setWorkingDir(self, working_dir):
        self.working_dir = working_dir
        self.lineEditWorkingDirectory.setText(self.working_dir)        

    def select_wcd(self):
        self.working_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        self.lineEditWorkingDirectory.setText(self.working_dir)        

    def close_dialog(self):
        self.close()     

    def entity_loaded(self, data):
        self.type = data["type"]
        self.project = data["project"]

        sections = []
        if self.type == "Shot":
            self.shot = data["item"]
            self.url = data["url"]

            if "code" in self.project:
                self.project_name = self.project["code"]
            else:
                self.project_name = self.project["name"]
            sections.append(self.project_name)
                
            if "episode_name" in self.shot:
                self.episode_name = self.shot["episode_name"]
                sections.append(self.episode_name)

            if "sequence_name" in self.shot:
                self.sequence_name = self.shot["sequence_name"]
                sections.append(self.sequence_name)

            self.shot_name = self.shot["name"] 
            sections.append(self.shot_name)
            self.lineEditEntity.setText(" / ".join(sections))
        else:
            self.setWindowTitle("swing: import asset")
            self.asset = data["item"]
            self.url = data["url"]

            if "code" in self.project:
                self.project_name = self.project["code"]
            else:
                self.project_name = self.project["name"]
            sections.append(self.project_name)  

            if "asset_type_name" in self.asset:
                self.asset_type_name = self.asset["asset_type_name"].strip()
                sections.append(self.asset_type_name)                 

            self.asset_name = self.entity["name"].strip() 
            sections.append(self.asset_name)

            sections.append(self.entity["name"].strip())

            self.lineEditEntity.setText(" / ".join(sections))

        namespace = "_".join(sections).lower().strip()

        #self.lineEditNamespace.setText(namespace)
        self.toolButtonWeb.setEnabled(self.url is not None)
        self.setEnabled(True)



def load_table_widget(tableWidget, files):
    model = []
    for item in files:
        model.append({
            "name": item,
            "size": "0",
            "status": "unknown"
        })

    tableWidget.setRowCount(len(model))

    row = 0
    for item in model:
        cell = QtWidgets.QTableWidgetItem(item["name"])
        cell.setData(QtCore.Qt.UserRole, item)

        cell.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        cell.setCheckState(QtCore.Qt.Checked)  
        tableWidget.setItem(row, 0, cell)

        if item["size"]:
            size = int(item["size"])
            if (size):
                cell = QtWidgets.QTableWidgetItem(human_size(size))
            else:
                cell = QtWidgets.QTableWidgetItem("")
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 1, cell)

        cell = QtWidgets.QTableWidgetItem("{}".format(item["status"]))
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 2, cell)

    tableWidget.setColumnWidth(0, 350)
    tableWidget.setColumnWidth(1, 100)
    tableWidget.setColumnWidth(2, 50)        

    return tableWidget
###########################################################################           

def load_settings(key, default):
    settings = QtCore.QSettings()    
    return settings.value(key, default)