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
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1


from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.background_workers import EntityFileLoader, EntityLoaderThread, FileDownloader
from wildchildanimation.gui.loader import LoaderDialogGUI
from wildchildanimation.gui.download_dialog import Ui_DownloadDialog

from wildchildanimation.gui.swing_tables import FileTableModel, setup_file_table
from wildchildanimation.gui.swing_utils import set_target, open_folder, human_size, set_button_icon

'''
    DownloadDialogGui class
    ################################################################################
'''

class DownloadDialogGUI(QtWidgets.QDialog, Ui_DownloadDialog):

    def __init__(self, parent, handler = None, file_list = None):
        super(DownloadDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setMinimumWidth(600)

        self.handler = handler

        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.file_list = file_list

        if self.file_list and len(self.file_list) > 0:
            self.load_files(self.file_list)
        
        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        set_button_icon(self.toolButtonAll, "../resources/fa-free/solid/plus.svg")
        self.toolButtonAll.clicked.connect(self.select_all)

        self.toolButtonNone.clicked.connect(self.select_none)
        set_button_icon(self.toolButtonNone, "../resources/fa-free/solid/minus.svg")

        self.tableView.doubleClicked.connect(self.file_table_double_click)

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
            working_dir = SwingSettings.get_instance().swing_root()
            set_target(self.selected_file, working_dir)

            if os.path.isfile(self.selected_file["target_path"]):
                reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(os.path.dirname(self.selected_file["target_path"]))
                    return True

            #self.close_dialog()

            self.loaderDialog = LoaderDialogGUI(parent = None, handler = self.handler, entity = self.entity)
            self.loaderDialog.load_files(self.file_list)
            self.loaderDialog.set_selected(self.selected_file)

            #dialog.exec_()
            self.loaderDialog.show()        

    def files_loaded(self, data):
        self.file_list = data[0]
        self.entity = data[1]

        self.load_files(self.file_list)        

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

    def file_loaded(self, results):
        status = results["status"]
        message = results["message"]
        size = results["size"]
        file_id = results["file_id"]
        #file_name = results["target"]
        #working_dir = results["working_dir"]

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
                break

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
        #message = result["message"]
        size = result["size"]
        file_id = result["file_id"]
        #file_name = result["target"]      

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
                break

    def load_files(self, file_list):
        self.tableModelFiles = FileTableModel(self, working_dir = SwingSettings.get_instance().swing_root(), items = file_list)
        setup_file_table(self.tableModelFiles, self.tableView)
        self.tableView.clicked.connect(self.select_row)   

    def select_row(self, index):
        self.tableView.model().setData(index, QtCore.Qt.Checked, QtCore.Qt.EditRole)
        self.tableView.model().layoutChanged.emit()    

    def on_click(self, index):
        row = index.row()
        column = 0

        row_item = self.tableView.item(row, column)
        selected = row_item.data(QtCore.Qt.UserRole)
        working_dir = SwingSettings.get_instance().swing_root()
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

        process_downloads(self, self.threadpool, file_list, self.progressBar, self.file_loading, self.file_loaded, skip_existing, extract_zips)                      

def process_downloads(parent, threadpool, file_list, progressBar = None, on_load = None, on_finished = None, skip_existing = True, extract_zips = True):
    if progressBar:
        progressBar.setRange(0, len(file_list))

    edit_api = "{}/edit".format(SwingSettings.get_instance().swing_server())
    working_dir = SwingSettings.get_instance().swing_root()

    downloads = 0
    row = 0
    for item in file_list:

        if "library-file" in item['file_type']:
            url = "{}/api/library_file/{}".format(edit_api, item["entity_id"])
            set_target(item, working_dir)
            worker = FileDownloader(parent, item["file_id"], url, item["target_path"], skip_existing, extract_zips, { "fn": item['file_name'] } )

            worker.callback.progress.connect(on_load)
            worker.callback.done.connect(on_finished)
            
            threadpool.start(worker)
            downloads += 1            

            item["status"] = "Busy"     

        elif "working-file" in item["file_type"]:
            url = "{}/api/working_file/{}".format(edit_api, item["file_id"])
            set_target(item, working_dir)

            worker = FileDownloader(parent, item["file_id"], url, item["target_path"], skip_existing, extract_zips)

            worker.callback.progress.connect(on_load)
            worker.callback.done.connect(on_finished)

            threadpool.start(worker)
            downloads += 1                

            item["status"] = "Busy"

        elif "output-file" in item["file_type"]:
            url = "{}/api/output_file/{}".format(edit_api, item["file_id"])
            set_target(item, working_dir)

            worker = FileDownloader(parent, item["file_id"], url, item["target_path"], skip_existing, extract_zips)

            worker.callback.progress.connect(on_load)
            worker.callback.done.connect(on_finished)

            threadpool.start(worker)
            ##debug
            ##worker.run()
            downloads += 1                

            item["status"] = "Busy"
        row = row + 1                   

    return downloads