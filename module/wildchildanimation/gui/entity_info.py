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
    from shiboken2 import wrapInstance 
    import PySide2.QtUiTools as QtUiTools
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    import sip
    qtMode = 1

import gazu

from datetime import datetime

import wildchildanimation.gui.background_workers as bg
from wildchildanimation.gui.image_loader import *

from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.loader import *
from wildchildanimation.gui.publish import *
from wildchildanimation.gui.downloads import *

from wildchildanimation.gui.entity_info_dialog import Ui_EntityInfoDialog
from wildchildanimation.gui.publish_dialog import Ui_PublishDialog

from wildchildanimation.gui.swing_tables import human_size, FileTableModel, setup_file_table

'''
    EntityInfoDialog class
    ################################################################################
'''

class EntityInfoDialog(QtWidgets.QDialog, Ui_EntityInfoDialog):

    working_dir = None
    
    def __init__(self, parent = None, entity = None, task_types = None, handler = None):
        super(EntityInfoDialog, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.entity = entity 
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.task_types = task_types
        self.file_list = None
        self.handler = handler
        self.tasks = None

        if self.entity:
            loader = bg.EntityLoaderThread(self, self.entity["id"], load_tasks = True)
            loader.callback.loaded.connect(self.entity_loaded)
            self.threadpool.start(loader)

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)            

        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonClose.clicked.connect(self.close_dialog)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)             

        #self.toolButtonAll.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogApplyButton))
        #self.toolButtonAll.clicked.connect(self.select_all)
        #self.toolButtonNone.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        #self.toolButtonNone.clicked.connect(self.select_none)

        self.tableView.doubleClicked.connect(self.file_table_double_click)
        self.pushButtonPublish.clicked.connect(self.publish)

        #self.toolButtonAll.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogApplyButton))
        self.toolButtonAll.clicked.connect(self.select_all)
        #self.toolButtonNone.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        self.toolButtonNone.clicked.connect(self.select_none)

        self.setWorkingDir(load_settings("projects_root", os.path.expanduser("~")))        

    def get_selected_task(self):
        if self.tasks:
            return self.tasks[self.comboBoxTasks.currentIndex()]
        return None

    def download_files(self):
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.pushButtonDownload.setText("Downloading")
        self.pushButtonDownload.setEnabled(False)
        
        self.pushButtonClose.setText("Busy")
        self.pushButtonClose.setEnabled(False)
        self.downloads = 0

        file_list = []
        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            if self.tableView.model().data(index, QtCore.Qt.DisplayRole):
                item = self.tableView.model().data(index, QtCore.Qt.UserRole)
                file_list.append(item)       

        self.progressBar.setRange(0, len(file_list))

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://example.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        row = 0
        for item in file_list:
            write_log("Downloading {}".format(item["name"]))

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

    def publish(self):
        task = self.get_selected_task()
        if task:        
            dialog = PublishDialogGUI(self, self.handler, gazu.task.get_task(task))
            dialog.setMinimumWidth(640)
            dialog.show()

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

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')              

    def entity_loaded(self, data):
        self.type = data["type"]
        self.shot = None
        self.asset = None
        self.project = data["project"]

        self.lineEditProject.setText(self.project["name"])
        # self.lineEditEntity.setEnabled(True)

        self.comboBoxTasks.setEnabled(True)
        self.pushButtonPublish.setEnabled(True)

        self.tasks = None
        if "tasks" in data["item"]:
            self.tasks = data["item"]["tasks"] 
            for task in self.tasks:
                task_type = self.get_item_task_type(task)
                self.comboBoxTasks.addItem(task_type["name"])
        self.comboBoxTasks.setEnabled(self.tasks is not None)

        ## ToDo: fix broken / missing history items
        if "history" in data:
            history = data["history"]
            if history:
                try:
                    history = sorted(history, key=lambda x: x["updated_at"], reverse=True)
                except:
                    pass
                for item in history:
                    if item:
                        comment = item["text"]
                        if comment and len(comment) > 0:
                            self.textEdit.append(comment.strip())

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

        if "preview_file_id" in self.entity and self.entity["preview_file_id"]:
            preview_file_id = self.entity["preview_file_id"]
            preview_file = gazu.files.get_preview_file(preview_file_id)

            #def __init__(self, parent, preview_file):
            #ef __init__(self, parent, server_api, email, password, preview_file):

            imageLoader = PreviewImageLoader(self, preview_file)
            imageLoader.callback.results.connect(self.load_preview_image)
            #imageLoader.run()
            self.threadpool.start(imageLoader)

            #print(preview_file_id)
            #self.load_preview_image(preview_url)

    def load_preview_image(self, pixmap):
        """
        Set the image to the pixmap
        :return:
        <img data-v-024ea0ea="" data-v-168620aa="" 
        class="thumbnail-picture asset-thumbnail flexrow-item" 
        data-src="/api/pictures/thumbnails/preview-files/1cc254f6-3381-4ac7-b3ec-a99dadd4c098.png" src="/api/pictures/thumbnails/preview-files/1cc254f6-3381-4ac7-b3ec-a99dadd4c098.png" lazy="loaded">
        """
        #response = requests.get(image_url)
        #data = response.content
        #pixmap = QtGui.QPixmap()
        #pixmap.loadFromData(data)
        #pixmap = pixmap.scaled(aspectMode=self.graphicsView.size().width, self.graphicsView.size().height,  QtCore.Qt.KeepAspectRatio)
        self.labelPreview.setPixmap(pixmap)            
        

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
                item["status"] = ""
                self.files.append(item)

        if working_files:
            for item in working_files:
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

        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            item = self.tableView.model().data(index, QtCore.Qt.UserRole)
            if file_id == item['id']:
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
            self.pushButtonClose.setText("Close")
            self.pushButtonClose.setEnabled(True)

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
            if file_id == item['id']:

                index = self.tableView.model().index(row, 5)
                download_status = {}
                download_status["message"] = "{}".format(human_size(size))
                download_status["color"] = QtGui.QColor('darkCyan')
                self.tableView.model().setData(index, download_status, QtCore.Qt.EditRole) 
                self.tableView.model().dataChanged.e 

    def load_files(self, file_list):
        self.tableModelFiles = FileTableModel(self, working_dir = load_settings("projects_root", os.path.expanduser("~")), files = file_list)
        setup_file_table(self.tableModelFiles, self.tableView)

    def file_table_double_click(self, index):
        row_index = index.row()
        self.selected_file = self.files[row_index]
        if self.selected_file:
            working_dir = load_settings("projects_root", os.path.expanduser("~"))
            set_target(self.selected_file, working_dir)

            if os.path.isfile(self.selected_file["target_path"]):
                reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(os.path.dirname(self.selected_file["target_path"]))
                    return True

            dialog = LoaderDialogGUI(self, self.handler, self.entity)
            dialog.load_files(self.files)
            dialog.set_selected(self.selected_file)
            #dialog.exec_()
            dialog.show()

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
        
        self.pushButtonClose.setText("Busy")
        self.pushButtonClose.setEnabled(False)
        self.downloads = 0

        file_list = []
        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            if self.tableView.model().data(index, QtCore.Qt.DisplayRole):
                item = self.tableView.model().data(index, QtCore.Qt.UserRole)
                file_list.append(item)       

        #write_log("Downloading {} files".format(len(file_list)))
        #write_log("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.progressBar.setRange(0, len(file_list))

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://example.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        row = 0
        for item in file_list:
            write_log("Downloading {}".format(item["name"]))

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

