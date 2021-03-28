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

from wildchildanimation.gui.swing_tables import human_size, FileTableModel

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

        #self.toolButtonAll.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogApplyButton))
        #self.toolButtonAll.clicked.connect(self.select_all)
        #self.toolButtonNone.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        #self.toolButtonNone.clicked.connect(self.select_none)

        self.tableViewFiles.doubleClicked.connect(self.file_table_double_click)
        self.pushButtonPublish.clicked.connect(self.publish)

    def get_selected_task(self):
        if self.tasks:
            return self.tasks[self.comboBoxTasks.currentIndex()]
        return None

    def download_files(self):
        dialog = DownloadDialogGUI(self, self.entity, self.task_types)
        dialog.resize(self.size())
        dialog.exec_()        

    def publish(self):
        task = self.get_selected_task()
        if task:        
            dialog = PublishDialogGUI(self, self.handler, gazu.task.get_task(task))
            dialog.setMinimumWidth(640)
            dialog.show()

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

        if "preview_file_id" in self.entity and self.entity["preview_file_id"]:
            preview_file_id = self.entity["preview_file_id"]
            preview_file = gazu.files.get_preview_file(preview_file_id)

            #def __init__(self, parent, preview_file):
            #ef __init__(self, parent, server_api, email, password, preview_file):

            imageLoader = PreviewImageLoader(self, preview_file)
            imageLoader.callback.results.connect(self.load_preview_image)
            imageLoader.run()

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

    def load_files(self, files):
        self.files = files

        tableModel = FileTableModel(self, self.files)

        # create the sorter model
        sorterModel = QtCore.QSortFilterProxyModel()
        sorterModel.setSourceModel(tableModel)
        sorterModel.setFilterKeyColumn(0)        

        self.tableViewFiles.setModel(sorterModel)                
        self.tableViewFiles.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableViewFiles.setSortingEnabled(True)
        self.tableViewFiles.sortByColumn(0, QtCore.Qt.DescendingOrder)

        #self.tableViewFiles.setColumnWidth(0, 300)
        #self.tableViewFiles.setColumnWidth(1, 150)
        #self.tableViewFiles.setColumnWidth(2, 75)
        #self.tableViewFiles.setColumnWidth(3, 150)
        #self.tableViewFiles.setColumnWidth(4, 350)
        #self.tableViewFiles.setColumnWidth(6, 200)

        hh = self.tableViewFiles.horizontalHeader()
        hh.setMinimumSectionSize(100)
        hh.setDefaultSectionSize(hh.minimumSectionSize())
        hh.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)          

        #selectionModel = self.tableViewFiles.selectionModel()
        #selectionModel.selectionChanged.connect(self.file_table_selection_changed)     

        self.tableViewFiles.verticalHeader().setDefaultSectionSize(self.tableViewFiles.verticalHeader().minimumSectionSize())          

        #selectionModel = self.tableViewFiles.selectionModel()
        #selectionModel.selectionChanged.connect(self.file_table_selection_changed)           

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

