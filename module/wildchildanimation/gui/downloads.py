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

from wildchildanimation.gui.background_workers import *

from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.loader import *

from wildchildanimation.gui.download_dialog import Ui_DownloadDialog

from wildchildanimation.gui.swing_tables import human_size, setup_file_table
from wildchildanimation.gui.swing_tables import FileTableModel, CheckBoxDelegate

'''
    DownloadDialogGui class
    ################################################################################
'''

class DownloadDialogGUI(QtWidgets.QDialog, Ui_DownloadDialog):

    working_dir = None
    
    def __init__(self, parent, handler = None, project_nav = None, entity = None, file_list = None):
        super(DownloadDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint ^ QtCore.Qt.WindowMinMaxButtonsHint)
        self.setMinimumWidth(600)
        self.nav = project_nav
        self.handler = handler
        self.entity = entity 
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.task_types = self.nav._task_types
        self.file_list = file_list
        self.swing_settings = SwingSettings.getInstance()

        if self.entity:
            loader = EntityLoaderThread(self, self.entity["id"])
            loader.callback.loaded.connect(self.entity_loaded)
            self.threadpool.start(loader)
        else:
            self.load_files(file_list)

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

        self.tableView.doubleClicked.connect(self.file_table_double_click)

        self.setWorkingDir(self.swing_settings.swing_root())

    def select_all(self):
        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            self.tableView.model().setData(index, True, QtCore.Qt.EditRole)
        self.tableView.update()

    def select_none(self):
        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            self.tableView.model().setData(index, False, QtCore.Qt.EditRole)
        self.tableView.update()

    def file_table_double_click(self, index):
        self.selected_file = self.tableView.model().data(index, QtCore.Qt.UserRole)        
        if self.selected_file:
            working_dir = self.swing_settings.swing_root()
            set_target(self.selected_file, working_dir)

            if os.path.isfile(self.selected_file["target_path"]):
                reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(os.path.dirname(self.selected_file["target_path"]))
                    return True

            dialog = LoaderDialogGUI(self, self.handler, self.entity)
            dialog.load_files(self.file_list)
            dialog.set_selected(self.selected_file)
            #dialog.exec_()
            dialog.show()        

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
            loader = EntityFileLoader(self, self.nav, self.shot, self.working_dir)

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
            loader = EntityFileLoader(self, self.nav, self.asset, self.working_dir)

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
        else:
            self.load_files(self.file_list)
            #loader.run()

    def get_item_task_type(self, entity):
        if "task_type_id" in entity:
            for task_type in self.task_types:
                if task_type["id"] == entity["task_type_id"]:
                    return task_type
        return None        

    def files_loaded(self, data):
        self.file_list = data[0]
        self.entity = data[1]

        self.load_files(self.file_list)        

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

        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            item = self.tableView.model().data(index, QtCore.Qt.UserRole)
            if file_id == item['file_id']:
                index = self.tableView.model().index(row, 5)
                download_status = {}
                download_status["message"] = "{} - {}".format(human_size(size), message)

                if "error" in status:
                    download_status["color"] = QtGui.QColor('darkRed')
                elif "skipped" in status:
                    download_status["color"] = QtGui.QColor('darkCyan')
                else:
                    download_status["color"] = QtGui.QColor('darkGreen')

                self.tableView.model().setData(index, download_status, QtCore.Qt.EditRole)     
                self.tableView.model().dataChanged.emit(index, index, QtCore.Qt.DisplayRole)                 
                self.tableView.viewport().update()

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

        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            item = self.tableView.model().data(index, QtCore.Qt.UserRole)
            if file_id == item['file_id']:

                index = self.tableView.model().index(row, 5)
                download_status = {}
                download_status["message"] = "{}".format(human_size(size))
                download_status["color"] = QtGui.QColor('darkCyan')
                self.tableView.model().setData(index, download_status, QtCore.Qt.EditRole) 
                self.tableView.model().dataChanged.emit(index, index, QtCore.Qt.DisplayRole)           
                self.tableView.viewport().update()      

    def load_files(self, file_list):
        self.tableModelFiles = FileTableModel(self, working_dir = self.swing_settings.swing_root(), items = file_list)
        setup_file_table(self.tableModelFiles, self.tableView)
        self.tableView.clicked.connect(self.select_row)   

    def select_row(self, index):
        self.tableView.model().setData(index, QtCore.Qt.Checked, QtCore.Qt.EditRole)
        self.tableView.model().layoutChanged.emit()    

    def on_click(self, index):
        row = index.row()
        column = 0
        # index.column()

        row_item = self.tableView.item(row, column)
        selected = row_item.data(QtCore.Qt.UserRole)
        working_dir = self.swing_settings.swing_root()
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
        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            if self.tableView.model().data(index, QtCore.Qt.DisplayRole):
                item = self.tableView.model().data(index, QtCore.Qt.UserRole)
                file_list.append(item) 

        skip_existing = self.checkBoxSkipExisting.isChecked()
        extract_zips = self.checkBoxExtractZips.isChecked()

        process_downloads(self, self.threadpool, file_list, self.progressBar, self.file_loading, self.file_loaded, self.working_dir, skip_existing, extract_zips)                      

def process_downloads(parent, threadpool, file_list, progressBar = None, on_load = None, on_finished = None, working_dir = None, skip_existing = True, extract_zips = True):
    if progressBar:
        progressBar.setRange(0, len(file_list))

    edit_api = "{}/edit".format(SwingSettings.getInstance().swing_server())

    downloads = 0
    row = 0
    for item in file_list:
        write_log("Downloading {}".format(item["file_name"]))

        if "library-file" in item['file_type']:
            url = "{}/api/library_file/{}".format(edit_api, item["entity_id"])
            set_target(item, working_dir)
            worker = FileDownloader(parent, working_dir, item["file_id"], url, item["target_path"], skip_existing, extract_zips, { "fn": item['file_name'] } )

            worker.callback.progress.connect(on_load)
            worker.callback.done.connect(on_finished)
            
            threadpool.start(worker)
            #worker.run()
            downloads += 1            

            item["status"] = "Busy"     

        elif "working-file" in item["file_type"]:
            url = "{}/api/working_file/{}".format(edit_api, item["file_id"])
            set_target(item, working_dir)

            worker = FileDownloader(parent, working_dir, item["file_id"], url, item["target_path"], skip_existing, extract_zips)

            worker.callback.progress.connect(on_load)
            worker.callback.done.connect(on_finished)

            threadpool.start(worker)
            #worker.run()
            downloads += 1                

            item["status"] = "Busy"

        elif "output-file" in item["file_type"]:
            url = "{}/api/output_file/{}".format(edit_api, item["file_id"])
            set_target(item, working_dir)

            worker = FileDownloader(parent, working_dir, item["file_id"], url, item["target_path"], skip_existing, extract_zips)

            worker.callback.progress.connect(on_load)
            worker.callback.done.connect(on_finished)

            threadpool.start(worker)
            #worker.run()
            downloads += 1                

            item["status"] = "Busy"
        row = row + 1                   

    return downloads