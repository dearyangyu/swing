# -*- coding: utf-8 -*-

import traceback
import sys
import os

import gazu

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtGui, QtCore, QtWidgets
    import sip
    qtMode = 1

from wildchildanimation.gui.background_workers import EntityFileLoader 
from wildchildanimation.gui.settings import SwingSettings    
from wildchildanimation.gui.image_loader import PreviewImageLoader

from wildchildanimation.gui.loader import EntityLoaderThread
from wildchildanimation.gui.downloads import process_downloads

from wildchildanimation.gui.entity_info_dialog import Ui_EntityInfoDialog

from wildchildanimation.gui.swing_utils import set_button_icon, set_target, open_folder, friendly_string
from wildchildanimation.gui.swing_tables import human_size, FileTableModel, setup_file_table

'''
    EntityInfoDialog class
    ################################################################################
'''

class EntityInfoDialog(QtWidgets.QDialog, Ui_EntityInfoDialog):

    working_dir = None
    
    def __init__(self, parent = None, entity = None, handler = None, task_types = None):
        super(EntityInfoDialog, self).__init__(parent) # Call the inherited classes __init__ method

        self.swing_settings = SwingSettings.get_instance()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint ^ QtCore.Qt.WindowMinMaxButtonsHint)
        self.read_settings()

        self.entity = entity 
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.task_types = task_types
        
        self.file_list = None
        self.handler = handler
        self.tasks = None
        self.file_list = []

        if self.entity:
            if isinstance(entity, dict):
                loader = EntityLoaderThread(self, self.entity["id"])
            else:
                loader = EntityLoaderThread(self, self.entity)

            loader.callback.loaded.connect(self.entity_loaded)
            self.threadpool.start(loader)

        set_button_icon(self.toolButtonWeb, "../resources/fa-free/solid/info-circle.svg")
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)            

        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonClose.clicked.connect(self.close_dialog)

        set_button_icon(self.toolButtonWorkingDir, "../resources/fa-free/solid/folder.svg")
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)             

        set_button_icon(self.toolButtonAll, "../resources/fa-free/solid/plus.svg")
        self.toolButtonAll.clicked.connect(self.select_all)

        set_button_icon(self.toolButtonNone, "../resources/fa-free/solid/minus.svg")
        self.toolButtonNone.clicked.connect(self.select_none)        

        self.tableView.doubleClicked.connect(self.file_table_double_click)
        self.pushButtonPublish.clicked.connect(self.publish)

        self.setWorkingDir(self.swing_settings.swing_root())        
        self.checkBoxCasted.clicked.connect(self.check_casted)

        self.checkBoxOutputFiles.clicked.connect(self.reload_files)
        self.checkBoxProjectFiles.clicked.connect(self.reload_files)
        self.checkBoxAllVersions.clicked.connect(self.reload_files)

    def reload_files(self):
        self.load_files(self.file_list)     

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("showBoxAllVersions", self.checkBoxAllVersions.isChecked())
        self.settings.setValue("showBoxCasted", self.checkBoxCasted.isChecked())
        self.settings.setValue("showBoxProjectFiles", self.checkBoxProjectFiles.isChecked())
        self.settings.setValue("showBoxOutputFiles", self.checkBoxOutputFiles.isChecked())        
        
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.project_root = self.settings.value("projects_root", os.path.expanduser("~"))
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))

        print(self.settings.value("showBoxAllVersions", True))

        self.checkBoxAllVersions.setChecked(self.is_setting_selected(self.settings, "showBoxAllVersions"))
        self.checkBoxCasted.setChecked(self.is_setting_selected(self.settings, "showBoxCasted"))
        self.checkBoxProjectFiles.setChecked(self.is_setting_selected(self.settings, "showBoxProjectFiles"))
        self.checkBoxOutputFiles.setChecked(self.is_setting_selected(self.settings, "showBoxOutputFiles"))

        self.settings.endGroup()  

    def is_setting_selected(self, settings, value):
        val = settings.value(value, True)
        return val == 'true'


    def check_casted(self):
        if self.entity:
            loader = EntityFileLoader(self, entity_id = self.entity["id"], working_dir = self.working_dir, task_types = self.task_types, show_hidden = False, scan_cast = self.checkBoxCasted.isChecked())
            loader.callback.loaded.connect(self.files_loaded)

            self.tableView.setEnabled(False)
            self.threadpool.start(loader)        
            # loader.run()

    def get_selected_task(self):
        return self.comboBoxTasks.currentData(QtCore.Qt.UserRole)

    def publish(self):
        task = self.get_selected_task()
        if task:     
            self.handler.on_publish(task = task, task_types = self.task_types)
            #dialog = PublishDialogGUI(self, task=task, task_types = self.task_types)

            #dialog = PublishDialogGUI(self, self.handler, gazu.task.get_task(task))
            #dialog.setMinimumWidth(640)
            #dialog.show()

    def select_count(self):
        count = 0
        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            if self.tableView.model().data(index):
                count += 1
        return count

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
        self.task_type_lookups = data["task_types"]

        self.type = data["type"]
        self.entity = data["entity"]
        ## self.task_types = data["task_types"]
        self.shot = None
        self.asset = None
        self.project = data["project"]

        self.lineEditProject.setText(self.project["name"])
        self.lineEditWorkingDirectory.setText(self.working_dir)

        # self.lineEditEntity.setEnabled(True)

        self.comboBoxTasks.setEnabled(True)
        self.pushButtonPublish.setEnabled(True)

        if "tasks" in data["item"]:
            self.tasks = data["item"]["tasks"] 
            for task in self.tasks:
                task["task_type"] = self.get_item_task_type(task, self.task_type_lookups)
                self.comboBoxTasks.addItem(task["task_type"]["name"], userData = task)
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
            loader = EntityFileLoader(self, self.shot["id"], self.working_dir, task_types = self.task_types, show_hidden = False, scan_cast = self.checkBoxCasted.isChecked())

            if "code" in self.project:
                sections.append(self.project["code"])
            else:
                sections.append(self.project["name"])

            if "episode_name" in self.shot:
                sections.append(self.shot["episode_name"])

            if "sequence_name" in self.shot:
                sections.append(self.shot["sequence_name"])

            sections.append(self.shot["name"])

            caption = " / ".join(sections)
            self.lineEditEntity.setText(caption)

            self.setWindowTitle("Shot Info: " + caption.upper())
        else:
            self.asset = data["item"]
            self.url = data["url"]
            self.labelEntity.setText("Asset")
            loader = EntityFileLoader(self, self.asset["id"], self.working_dir, task_types = self.task_types, show_hidden = False, scan_cast = self.checkBoxCasted.isChecked())

            if "code" in self.project:
                sections.append(self.project["code"])
            else:
                sections.append(self.project["name"])            

            if "asset_type_name" in self.asset:
                sections.append(self.asset["asset_type_name"].strip())                 

            sections.append(self.entity["name"].strip())

            caption = " / ".join(sections)
            self.lineEditEntity.setText(caption)

            self.setWindowTitle("Asset Info: " + caption.upper())

        self.toolButtonWeb.setEnabled(self.url is not None)
        self.setEnabled(True)

        if not self.file_list:
            loader.callback.loaded.connect(self.files_loaded)
            self.threadpool.start(loader)
        else:
            self.load_files(self.file_list)

        if "preview_file_id" in self.entity and self.entity["preview_file_id"]:
            preview_file_id = self.entity["preview_file_id"]

            imageLoader = PreviewImageLoader(self, preview_file_id)
            imageLoader.callback.results.connect(self.load_preview_image)
            self.threadpool.start(imageLoader)

    def load_preview_image(self, pixmap):
        self.labelPreview.setPixmap(pixmap)            
        
    def get_item_task_type(self, entity, task_type_lookups):
        if "task_type_id" in entity:
            for task_type in task_type_lookups:
                if task_type["id"] == entity["task_type_id"]:
                    return task_type
        return None        

    def files_loaded(self, data):
        self.file_list = data[0]
        if len(self.file_list) > 0:
            self.tableView.setEnabled(True)        
            self.load_files(self.file_list)        
        else:
            self.tableView.setEnabled(False)        

    def setWorkingDir(self, working_dir):
        self.working_dir = working_dir

    def set_selected(self, file_item):
        if not file_item:
            return
        
        index = 0
        while index < len(self.file_list):
            if file_item["id"] == self.file_list[index]["id"]:
                break
            index += 1        

    def close_dialog(self):
        self.write_settings()
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


    def load_files(self, files_loaded):
        self.file_list = files_loaded

        # build a hashmap using file name
        file_map = {}
        for item in files_loaded:
            item_key = "{}{}{}".format(item["entity_id"], item["task_type_id"], item["file_type"])

            if not item_key in file_map:
                file_map[item_key] = []

            file_versions = file_map[item_key]
            file_versions.append(item)

            file_map[item_key] = sorted(file_versions, key = lambda x: x["file_updated_at"], reverse = True)
            # item["file_revision"] > current["file_revision"]:    
            #         

        file_list = []

        for file_name in file_map.keys():
            file_versions = file_map[file_name]
        
            version_added = False
            for item in file_versions:
                if "output" in item["file_type"]:
                    if not self.checkBoxOutputFiles.isChecked():
                        continue # skip output files

                if "working" in item["file_type"]:
                    if not self.checkBoxProjectFiles.isChecked():
                        continue # skip working file

                if "task_type_id" in item:
                    task_type_id = item["task_type_id"]

                    found = False
                    for tt in self.task_types:
                        if task_type_id == tt["id"]:
                            found = True
                            break

                    if not found:
                        continue

                if self.checkBoxAllVersions.isChecked():
                    file_list.append(item)
                else:
                    if not version_added:
                        file_list.append(item)
                        version_added = True


        self.tableModelFiles = FileTableModel(self, working_dir = self.swing_settings.swing_root(), items = file_list)
        setup_file_table(self.tableModelFiles, self.tableView)

    def get_casted_namespace(self, resource):
        print("Checking casted namespace")
        sections = []

        if "code" in self.project:
            self.project_name = self.project["code"]
        else:
            self.project_name = self.project["name"]
        sections.append(self.project_name)                                

        if resource["type"] == "Shot":
            sections.append(resource["parent"])
            sections.append(resource["entity"])
            return friendly_string("_".join(sections).lower())
        else:
            entity_type_name = resource["type"]

            # check if we have a shortened form of the name
            if entity_type_name in self.handler.ASSET_TYPE_LOOKUP:
                entity_type_name = self.handler.ASSET_TYPE_LOOKUP[entity_type_name]

            sections.append(entity_type_name)
            sections.append(friendly_string(resource["entity"]))

            return friendly_string("_".join(sections).lower())            


    def file_table_double_click(self, index):
        self.selected_file = self.tableView.model().data(index, QtCore.Qt.UserRole)  
        ##print(self.selected_file)      

        if self.selected_file:
            working_dir = self.swing_settings.swing_root()
            set_target(self.selected_file, working_dir)

            if os.path.isfile(self.selected_file["target_path"]):
                reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(os.path.dirname(self.selected_file["target_path"]))
                    return True

            if self.checkBoxCasted.isChecked():
                namespace = self.get_casted_namespace(self.selected_file)
            else:
                namespace = False

            self.handler.on_load(parent = self, entity = self.entity, files = self.file_list, selected = self.selected_file, namespace = namespace)
            # self.handler.on_load()

            #self.loaderDialog = LoaderDialogGUI(parent = self.parentWidget(), handler = self.handler, entity = self.entity)
            #self.loaderDialog.load_files(self.file_list)
            #self.loaderDialog.set_selected(self.selected_file)
            ##dialog.exec_()
            #self.loaderDialog.show()

    def on_click(self, index):
        selected = self.tableView.model().data(index, QtCore.Qt.UserRole)      
        working_dir = self.swing_settings.swing_root()
        set_target(selected, working_dir)        

        if os.path.exists(selected["target_path"]):
            reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                open_folder(os.path.dirname(selected["target_path"]))

    def download_files(self):
        if self.select_count() == 0:
            self.select_all()
             
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

        skip_existing = self.checkBoxSkipExisting.isChecked()
        extract_zips = self.checkBoxExtractZips.isChecked()

        process_downloads(self, self.threadpool, file_list, self.progressBar, self.file_loading, self.file_loaded, skip_existing, extract_zips) 

### end of class

