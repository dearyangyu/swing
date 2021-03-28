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

import wildchildanimation.gui.background_workers as bg

from wildchildanimation.gui.swing_utils import *

from wildchildanimation.gui.download_dialog import Ui_DownloadDialog

from wildchildanimation.gui.swing_tables import human_size, load_file_table_widget

'''
    DownloadDialogGui class
    ################################################################################
'''

class DownloadDialogGUI(QtWidgets.QDialog, Ui_DownloadDialog):

    working_dir = None
    
    def __init__(self, parent = None, entity = None, task_types = None, file_list = None):
        super(DownloadDialogGUI, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.entity = entity 
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.task_types = task_types
        self.file_list = file_list

        if self.entity:
            loader = bg.EntityLoaderThread(self, self.entity["id"])
            loader.callback.loaded.connect(self.entity_loaded)
            self.threadpool.start(loader)

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)               

        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        #self.toolButtonAll.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogApplyButton))
        self.toolButtonAll.clicked.connect(self.select_all)
        #self.toolButtonNone.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
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
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')              

    def entity_loaded(self, data):
        self.type = data["type"]
        self.shot = None
        self.asset = None
        self.project = data["project"]

        sections = []
        if self.type == "Shot":
            self.shot = data["item"]
            self.url = data["url"]
            self.labelEntity.setText("Shot")
            loader = bg.EntityFileLoader(self, self.shot, self.working_dir)

            if "code" in self.project:
                sections.append(self.project["code"])
            else:
                sections.append(self.project["name"])
            sections.append("shots")

            if "episode_name" in self.shot:
                sections.append(self.shot["episode_name"])

            if "sequence_name" in self.shot:
                sections.append(self.shot["sequence_name"])

            sections.append(self.shot["name"])
            self.lineEditEntity.setText(" / ".join(sections))
        else:
            self.asset = data["item"]
            self.url = data["url"]
            self.labelEntity.setText("Asset")
            loader = bg.EntityFileLoader(self, self.asset, self.working_dir)

            if "code" in self.project:
                sections.append(self.project["code"])
            else:
                sections.append(self.project["name"])            
            sections.append("assets")

            if "asset_type_name" in self.asset:
                sections.append(self.asset["asset_type_name"].strip())                 

            sections.append(self.entity["name"].strip())

            self.lineEditEntity.setText(" / ".join(sections))

        self.toolButtonWeb.setEnabled(self.url is not None)
        self.setEnabled(True)

        if not self.file_list:
            loader.callback.loaded.connect(self.files_loaded)
            self.threadpool.start(loader)

    def get_item_task_type(self, entity):
        if "task_type_id" in entity:
            for task_type in self.task_types:
                if task_type["id"] == entity["task_type_id"]:
                    return task_type
        return None        

    def files_loaded(self, data):
        self.file_list = data

        output_files = data["output_files"]
        working_files = data["working_files"]

        self.files = []
        if output_files:
            for item in output_files:
                item["task_type"] = self.get_item_task_type(item)
                item["status"] = ""
                self.files.append(item)

        if working_files:
            for item in working_files:
                item["task_type"] = self.get_item_task_type(item)                
                item["status"] = ""
                self.files.append(item)        

        self.load_files(self.files)        


    def setWorkingDir(self, working_dir):
        self.working_dir = working_dir
        self.lineEditWorkingDirectory.setText(self.working_dir)

    def set_selected(self, file_item):
        if not file_item:
            return
        
        index = 0
        while index < len(self.files):
            if file_item["id"] == self.files[index]["id"]:
                break
            index += 1        

    def close_dialog(self):
        self.close()

    def select_wcd(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if (q):
            self.setWorkingDir(q[0])

    def file_loaded(self, results):
        status = results["status"]
        message = results["message"]
        size = results["size"]
        file_id = results["file_id"]
        file_name = results["target"]
        working_dir = results["working_dir"]

        index = 0
        while index < self.tableWidget.rowCount():
            row_item = self.tableWidget.item(index, 0)
            file_item = row_item.data(QtCore.Qt.UserRole)
            if file_item and file_id == file_item["id"]:
                status_item = self.tableWidget.item(self.tableWidget.row(row_item), 5)
                status_item.setText("{} - {}".format(human_size(size), message))

                if "error" in status:
                    status_item.setBackground(QtGui.QColor('darkRed'))
                elif "skipped" in status:
                    status_item.setBackground(QtGui.QColor('darkCyan'))
                else:
                    status_item.setBackground(QtGui.QColor('darkGreen'))
                break        

            index += 1

        self.downloads -= 1
        if self.downloads <= 0:
            self.pushButtonCancel.setText("Close")
            self.pushButtonCancel.setEnabled(True)

            self.pushButtonDownload.setText("Download")
            self.pushButtonDownload.setEnabled(True)
            self.progressBar.setRange(0, 1)
        else:
            self.progressBar.setValue(self.progressBar.value() + 1)


    def file_loading(self, result):
        message = result["message"]
        size = result["size"]
        file_id = result["file_id"]
        file_name = result["target"]        

        index = 0
        while index < self.tableWidget.rowCount():
            row_item = self.tableWidget.item(index, 0)
            file_item = row_item.data(QtCore.Qt.UserRole)
            if file_item and file_id == file_item["id"]:
                status_item = self.tableWidget.item(self.tableWidget.row(row_item), 5)
                status_item.setText("{}".format(human_size(size)))
                status_item.setBackground(QtGui.QColor('darkCyan'))
                break
            index += 1        

    def load_files(self, files):
        self.files = files

        self.tableWidget = load_file_table_widget(self.tableWidget, files)
        self.tableWidget.doubleClicked.connect(self.on_click) 

    def on_click(self, index):
        row = index.row()
        column = index.column()

        row_item = self.tableWidget.item(row, column)
        selected = row_item.data(QtCore.Qt.UserRole)
        working_dir = load_settings("projects_root", os.path.expanduser("~"))
        set_target(selected, working_dir)        

        if os.path.exists(selected["target_path"]):
            reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                open_folder(os.path.dirname(selected["target_path"]))

    def download_files(self):
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.pushButtonDownload.setText("Downloading")
        self.pushButtonDownload.setEnabled(False)
        
        self.pushButtonCancel.setText("Busy")
        self.pushButtonCancel.setEnabled(False)
        self.downloads = 0

        file_list = []

        index = 0
        while index < self.tableWidget.rowCount():
            row_item = self.tableWidget.item(index, 0)
            if row_item.checkState():
                file_list.append(row_item.data(QtCore.Qt.UserRole))
            index += 1

        #write_log("Downloading {} files".format(len(file_list)))
        #write_log("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.progressBar.setRange(0, index)

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://production.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        row = 0
        for item in file_list:
            write_log("Downloading {} to {}".format(item["name"], self.working_dir))

            if "WorkingFile" in item["type"]:
                url = "{}/api/working_file/{}".format(edit_api, item["id"])
                target = set_target(item, self.working_dir)

                worker = bg.FileDownloader(self, self.working_dir, item["id"], url, item["target_path"], email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

                worker.callback.progress.connect(self.file_loading)
                worker.callback.done.connect(self.file_loaded)
                self.threadpool.start(worker)
                self.downloads += 1                
                item["status"] = "Busy"
            else:
                url = "{}/api/output_file/{}".format(edit_api, item["id"])
                target = set_target(item, self.working_dir)

                worker = bg.FileDownloader(self, self.working_dir, item["id"], url, item["target_path"], email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

                worker.callback.progress.connect(self.file_loading)
                worker.callback.done.connect(self.file_loaded)
                
                self.threadpool.start(worker)
                self.downloads += 1            

                item["status"] = "Busy"
            row = row + 1        
