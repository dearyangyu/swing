# -*- coding: utf-8 -*-
# PyQt Gui plugin for Treehouse
#
# version: 1.000
# date: 18 Feb 2021
#
#############################
_APP_NAME = "treehouse: swing"
_APP_VERSION = "0.0.7"
 
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

import keyring
import gazu
import os.path
from datetime import datetime

import requests

import wildchildanimation.background_workers as bg

from wildchildanimation.gui.swing_utils import *

from wildchildanimation.gui.main_form import Ui_WcaMayaDialog
from wildchildanimation.gui.connection_dialog import Ui_ConnectionDialog
from wildchildanimation.gui.publish_dialog import Ui_PublishDialog

from wildchildanimation.gui.loader_dialog import Ui_LoaderDialog
from wildchildanimation.gui.create_dialog import Ui_CreateDialog
from wildchildanimation.gui.upload_monitor_dialog import Ui_UploadMonitorDialog
from wildchildanimation.gui.playblast_dialog import Ui_PlayblastDialog
from wildchildanimation.gui.zurbrigg_playblast import *

from wildchildanimation.gui.references import *
from wildchildanimation.gui.search import *
from wildchildanimation.gui.downloads import *
from wildchildanimation.gui.breakout import *

from wildchildanimation.gui.swing_tables import FileTableModel, TaskTableModel, CastingTableModel, load_file_table_widget, human_size

'''
    SwingGUI Main class
    ################################################################################
'''
class SwingGUI(QtWidgets.QDialog, Ui_WcaMayaDialog):
    loading = False
    user_email = None
    tasks = []
    task_types = []

    first_load = True

    currentProject = None
    currentEpisode = None
    currentSequences = None
    currentSequencesIndex = None
    currentShot = None
    currentTask = None
    currentAssetType = None
    currentAsset = None
    gazu_client = None
    connected = False
    project_root = None
    currentWorkingDir = None

    selected_file = None
    selected_task = None

    def __init__(self, studio_handler = None):
        super(SwingGUI, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.handler = studio_handler
        self.connect(self, QtCore.SIGNAL("finished(int)"), self.finished)
        self.setWindowTitle("{} v{}".format(_APP_NAME, _APP_VERSION))

        resource_file = resource_path("resources/TreeHouse_Logo_no_text.png")
        if os.path.exists(resource_file):
            icon = QtGui.QIcon(resource_file)
            self.setWindowIcon(icon)

        QtCore.QCoreApplication.setOrganizationName("Wild Child Animation")
        QtCore.QCoreApplication.setOrganizationDomain("wildchildanimation.com")
        QtCore.QCoreApplication.setApplicationName(_APP_NAME)
        
        self.comboBoxAsset.currentIndexChanged.connect(self.load_asset_files)
        self.comboBoxShot.currentIndexChanged.connect(self.load_shot_files)    

        self.pushButtonSettings.clicked.connect(self.open_connection_settings)
        self.pushButtonConnect.clicked.connect(self.connect_to_server)
        self.pushButtonRefresh.clicked.connect(self.refresh_data)

        self.pushButtonImport.clicked.connect(self.load_asset)
        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonPublish.clicked.connect(self.publish_scene)
        self.pushButtonPlayblast.clicked.connect(self.playblast_scene)
        self.pushButtonNew.clicked.connect(self.new_scene)
        self.pushButtonSearchFiles.clicked.connect(self.search_files_dialog)
        self.pushButtonBreakout.clicked.connect(self.breakout_dialog)
        #self.setWorkingDir(load_settings("projects_root", os.path.expanduser("~")))


        self.pushButtonClose.clicked.connect(self.close_dialog)

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.comboBoxSequence.currentIndexChanged.connect(self.sequence_changed)
        self.comboBoxAssetType.currentIndexChanged.connect(self.asset_type_changed)      

        self.radioButtonShot.toggled.connect(self.set_to_shot)
        self.radioButtonAsset.toggled.connect(self.set_to_asset)

        #self.treeWidgetFiles.doubleClicked.connect(self.open_file_item)
        self.tableViewFiles.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewFiles.doubleClicked.connect(self.file_table_double_click)

        self.readSettings()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        if self.connect_to_server():
            self.labelConnection.setText("Connected")
            self.refresh_data()

    def keyPressEvent(self, event):
        super(SwingGUI, self).keyPressEvent(event)

        event.accept()

    def finished(self, code):
        write_log('we are finished %s\n' % str(code))            


    def open_file_item(self, index):
        item = self.treeWidgetFiles.itemFromIndex(index)

        if not item:
            return False

        file_name = item.data(index.row(), 0)
        
        working_dir = load_settings("projects_root", os.path.expanduser("~"))
        file_item = os.path.join(os.path.join(file_name, working_dir))

        file_list = self.get_file_selection_list()

        dialog = LoaderDialogGUI(self)
        dialog.load_files(file_list)
        dialog.set_file_name(file_name)
        dialog.show()        
        

    def set_loading(self, is_loading):
        self.loading = is_loading

        if self.loading:
            self.progressBar.setMaximum(0)
        else:
            self.progressBar.setMaximum(1)

        self.comboBoxEpisode.setEnabled(not is_loading)
        self.comboBoxSequence.setEnabled(not is_loading)
        self.comboBoxShot.setEnabled(not is_loading)
        self.comboBoxAssetType.setEnabled(not is_loading)
        self.radioButtonAsset.setEnabled(not is_loading)
        self.radioButtonShot.setEnabled(not is_loading)
        self.tabWidget.setEnabled(not is_loading)


    def set_to_shot(self):
        self.comboBoxShot.setEnabled(self.radioButtonShot.isChecked())
        self.radioButtonAsset.setChecked(False)

        if self.radioButtonShot.isChecked() and (self.currentSequencesIndex is not None) and len(self.currentSequences[self.currentSequencesIndex]["shots"]) > 0:
            self.load_shot_files(0)

    def set_to_asset(self):
        self.comboBoxAsset.setEnabled(self.radioButtonAsset.isChecked())
        self.comboBoxAssetType.setEnabled(self.radioButtonAsset.isChecked())
        self.comboBoxShot.setEnabled(False)

        if self.radioButtonAsset.isChecked():
            if self.currentAsset:
                self.load_asset_files(0)
            else:
                if self.currentAssetType:
                    self.asset_type_changed(self.comboBoxAssetType.currentIndex())
                else:
                    asset_loader = bg.AssetTypeLoaderThread(self, self.currentProject)
                    asset_loader.callback.loaded.connect(self.asset_types_loaded)
                    self.threadpool.start(asset_loader)

    def get_current_selection(self):
        if self.radioButtonAsset.isChecked():
            return self.currentAsset
        else:
            return self.currentShot

    # save main dialog state
    def writeSettings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.endGroup()

        self.settings.beginGroup("Selection")

        if self.currentProject:
            self.settings.setValue("last_project", self.currentProject["id"])

        if self.currentSequencesIndex and len(self.currentSequences) > 0 and self.currentSequences[self.currentSequencesIndex]:
            self.settings.setValue("last_sequences", self.currentSequences[self.currentSequencesIndex]["id"])

        if self.currentShot:
            self.settings.setValue("last_shot", self.currentShot["id"])

        self.settings.endGroup()        

    # load main dialog state
    def readSettings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size", QtCore.QSize(400, 400)))
        self.move(self.settings.value("pos", QtCore.QPoint(200, 200)))
        self.settings.endGroup()            

        self.settings.beginGroup("Selection")

        self.last_project = self.settings.value("last_project")
        self.last_sequences = self.settings.value("last_project")
        self.last_shot = self.settings.value("last_project")
        self.settings.endGroup()          

        self.settings.beginGroup("Workplace")
        self.project_root = self.settings.value("projects_root")
        self.ffmpeg_bin = self.settings.value("ffmpeg_bin")
        self.settings.endGroup()         
    
    def open_connection_settings(self):
        dialog = ConnectionDialogGUI(self)

        dialog.lineEditServer.setText(load_settings('server', 'https://production.wildchildanimation.com'))
        dialog.lineEditEmail.setText(load_settings('user', 'user@example.com'))
        dialog.lineEditProjectsFolder.setText(load_settings('projects_root', os.path.expanduser("~")))
        dialog.lineEditPassword.setText(load_keyring('swing', 'password', 'Not A Password'))

        dialog.exec_()
        write_log("loading settings")

    def connect_to_server(self): 
        if self.connected and self.gazu_client:
            self.gazu_client = None
            self.connected = False

        password = load_keyring('swing', 'password', 'Not A Password')

        server = load_settings('server', 'https://production.wildchildanimation.com')
        email = load_settings('user', 'user@example.com')

        gazu.set_host("{}/api".format(server))
        try:
            self.gazu_client = gazu.log_in(email, password)
            self.connected = True
            self.user_email = email
            self.pushButtonConnect.setText("Connected")

            self.refresh_data()
        except:
            self.pushButtonConnect.setText("Reconnect")
            return False

        return True

    def close_dialog(self):
        self.close()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Exit Application', 'Are you sure ?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.writeSettings()
            event.accept()
        else:
            event.ignore()        

    def refresh_data(self):
        write_log("[refresh_data]")

        if not self.loading:
            self.comboBoxProject.blockSignals(True)
            loader = bg.ProjectLoaderThread(self)
            loader.callback.loaded.connect(self.projects_loaded)

            self.progressBar.setMaximum(0)
            self.set_loading(True)

            self.threadpool.start(loader)
        else:
            write_log("Loading in progress")

    def projects_loaded(self, results): 
        write_log("[projects_loaded]")
        #self.comboBoxProject.setEnabled(True)

        self.progressBar.setMaximum(1)

        self.projects = results["projects"]
        self.task_types = results["task_types"]

        self.comboBoxProject.clear()
        self.currentProjectIndex = 0

        index = 0
        for item in self.projects:
            self.comboBoxProject.addItem(item["name"])

            if self.last_project and self.last_project == item["id"]:
                self.currentProjectIndex = index
            index += 1

        self.comboBoxProject.blockSignals(False)      

        if self.currentProjectIndex:
            self.comboBoxProject.setCurrentIndex(self.currentProjectIndex)
            #self.project_changed(self.currentProjectIndex)   
            # 
        if self.first_load:
            self.first_load = False
            self.project_changed(self.currentProjectIndex)   

    def project_changed(self, index):
        write_log("[project_changed]")

        self.currentProject = self.projects[index]
        self.currentProjectIndex = index

        self.comboBoxEpisode.clear()
        self.comboBoxSequence.clear()
        self.comboBoxShot.clear()
        self.comboBoxAssetType.clear()

        if self.currentProject:
            self.progressBar.setMaximum(0)
            self.set_loading(True)                

            loader = bg.ProjectHierarchyLoaderThread(self, self.currentProject)
            loader.callback.loaded.connect(self.hierarchy_loaded)
            self.threadpool.start(loader)

            asset_loader = bg.AssetTypeLoaderThread(self, self.currentProject)
            asset_loader.callback.loaded.connect(self.asset_types_loaded)
            self.threadpool.start(asset_loader)

            task_loader = bg.TaskLoaderThread(self, self.currentProject, self.user_email)
            task_loader.callback.loaded.connect(self.tasks_loaded)
            self.threadpool.start(task_loader)


    def hierarchy_loaded(self, data): 
        write_log("[hierarchy_loaded]")
        self.progressBar.setMaximum(1)

        self.episodes = data

        self.comboBoxEpisode.blockSignals(True)
        for item in self.episodes:
            self.comboBoxEpisode.addItem(item["name"])

        self.comboBoxEpisode.setEnabled(len(self.episodes) > 0)
        self.comboBoxEpisode.blockSignals(False)

        if len(self.episodes) > 0:
            self.episode_changed(0)
        else:
            self.asset_type_changed(0)

        self.set_loading(False)

        
    def episode_changed(self, index):
        write_log("[episode_changed]")
        self.currentEpisode = self.episodes[index]
        self.currentEpisodeIndex = index

        if self.currentEpisode:
            self.comboBoxSequence.blockSignals(True)
            self.comboBoxSequence.clear()
            for item in self.currentEpisode["sequences"]:
                self.comboBoxSequence.addItem(item["name"])          
            self.comboBoxSequence.blockSignals(False)    

            if len(self.currentEpisode["sequences"]) > 0:
                self.comboBoxSequence.setEnabled(True)
                self.sequence_changed(0)

    def asset_types_loaded(self, data): 
        write_log("[asset_types_loaded]")
        self.asset_types = data

        self.comboBoxAssetType.blockSignals(True)
        self.comboBoxAssetType.clear()
        for item in self.asset_types:
            #name = "{} {}".format(self.currentProject["code"], item["name"])            
            self.comboBoxAssetType.addItem(item["name"]) 
        self.comboBoxAssetType.blockSignals(False)                       
        self.comboBoxAssetType.setEnabled(True)

        if len(self.asset_types) > 0:
            self.asset_type_changed(0)

    def tasks_loaded(self, data):
        write_log("[tasks_loaded]")

        self.tasks = data
        self.load_tasks(self.tasks)

    def sequence_changed(self, index):
        write_log("[sequence_changed]")
        
        self.currentSequencesIndex = self.comboBoxSequence.currentIndex()
        self.currentSequences = self.currentEpisode["sequences"]
        self.currentEpisode["sequences"][self.currentSequencesIndex]

        self.comboBoxShot.blockSignals(True)                 
        self.comboBoxShot.clear()

        for item in self.currentSequences[self.currentSequencesIndex]["shots"]:
            #name = "{} {}".format(item["sequence_name"],  item["name"])
            self.comboBoxShot.addItem(item["name"]) 
        self.comboBoxShot.blockSignals(False)                 

        if len(self.currentSequences[self.currentSequencesIndex]["shots"]) > 0:
            if self.radioButtonShot.isChecked():
                self.comboBoxShot.setEnabled(True)
                self.load_shot_files(0)

    def asset_type_changed(self, index):
        write_log("[asset_type_changed]")
        self.currentAssetType = self.asset_types[index]

        loader = bg.AssetLoaderThread(self, self.currentProject, self.currentAssetType)
        loader.callback.loaded.connect(self.asset_loaded)
        self.threadpool.start(loader)

    def load_shot_files(self, index):
        self.currentShot = self.currentSequences[self.currentSequencesIndex]["shots"][index]
        write_log("load shot files {}".format(index))

        loader = bg.EntityFileLoader(self, self.currentShot, working_dir = load_settings("projects_root", os.path.expanduser("~")))
        loader.callback.loaded.connect(self.files_loaded)
        self.threadpool.start(loader)

    def files_loaded(self, data):
        output_files = data["output_files"]
        working_files = data["working_files"]

        self.load_files(output_files, working_files)        
        write_log("Loaded {} output files, {} working files".format(len(output_files), len(working_files)))

    def asset_loaded(self, data): 
        write_log("[asset_loaded]")

        self.assets = data
        self.comboBoxAsset.clear()

        last = self.comboBoxAsset.currentIndex()
        for p in self.assets:
            name = ""

            #if self.currentProject:
            #    name = "{} {}".format(name, self.currentProject["code"])

            #if self.currentEpisode:
            #    name = "{} {}".format(name, self.currentEpisode["name"])

            #if self.currentSequences and self.currentSequencesIndex and len(self.currentSequences) > 0:
            #    name = "{} {}".format(name, self.currentSequences[self.currentSequencesIndex]["name"])

            name = "{} {}".format(name, p["name"]).strip()
            self.comboBoxAsset.addItem(name)     
        self.comboBoxAsset.setEnabled(True)       

    def load_asset_files(self, index):
        self.currentAsset = self.assets[index]

        write_log("load asset files {}".format(index))
        loader = bg.EntityFileLoader(self, self.currentAsset, working_dir = load_settings("projects_root", os.path.expanduser("~")))
        loader.callback.loaded.connect(self.files_loaded)
        self.threadpool.start(loader)       

    def load_files(self, output_files = None, working_files = None):
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

        self.tableViewFiles.setModel(FileTableModel(self, self.files))                
        self.tableViewFiles.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableViewFiles.setColumnWidth(0, 300)
        self.tableViewFiles.setColumnWidth(1, 75)
        self.tableViewFiles.setColumnWidth(2, 75)
        self.tableViewFiles.setColumnWidth(3, 150)
        #self.tableViewFiles.setColumnWidth(4, 350)
        #self.tableViewFiles.setColumnWidth(6, 200)

        selectionModel = self.tableViewFiles.selectionModel()
        selectionModel.selectionChanged.connect(self.file_table_selection_changed)       

        self.pushButtonDownload.setEnabled(len(self.files) > 0)    
        self.pushButtonImport.setEnabled(len(self.files) > 0)

    def file_table_double_click(self, index):
        row_index = index.row()
        self.selected_file = self.tableViewFiles.model().files[row_index]
        if self.selected_file:
            working_dir = load_settings("projects_root", os.path.expanduser("~"))
            set_target(self.selected_file, working_dir)

            if os.path.isfile(self.selected_file["target_path"]):
                reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(os.path.dirname(self.selected_file["target_path"]))
                    return True

            dialog = LoaderDialogGUI(self, self.handler, self.get_current_selection())
            dialog.load_files(self.tableViewFiles.model().files)
            dialog.set_selected(self.selected_file)
            #dialog.exec_()
            dialog.show()


    def file_table_selection_changed(self):
        if not (self.tableViewFiles.selectedIndexes()):
            return False

        idx = self.tableViewFiles.selectedIndexes()
        for index in idx:
            row_index = index.row()
            try:
                self.selected_file = self.tableViewFiles.model().files[row_index]
                self.pushButtonLoad.setEnabled(self.selected_file is not None)
                self.pushButtonImport.setEnabled(self.selected_file is not None)

            except:
                pass

        return True

    def get_item_task_type(self, entity):
        if "task_type_id" in entity:
            for task_type in self.task_types:
                if task_type["id"] == entity["task_type_id"]:
                    return task_type
        return None

    def load_tasks(self, tasks = None):
        model = TaskTableModel(self, tasks)

        self.tableViewTasks.setModel(model)
        self.tableViewTasks.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableViewTasks.setColumnWidth(0, 250)
        self.tableViewTasks.setColumnWidth(1, 200)
        self.tableViewTasks.setColumnWidth(2, 250)
        self.tableViewTasks.setColumnWidth(3, 350)
        self.tableViewTasks.setColumnWidth(4, 120)

        selectionModel = self.tableViewTasks.selectionModel()
        selectionModel.selectionChanged.connect(self.task_table_selection_changed)          

        # self.pushButtonPublish.setEnabled(len(tasks) > 0)

    def task_table_selection_changed(self):
        if not (self.tableViewTasks.selectedIndexes()):
            return False

        idx = self.tableViewTasks.selectedIndexes()
        for index in idx:
            row_index = index.row()
            try:
                self.selected_task = self.tableViewTasks.model().tasks[row_index]

                self.pushButtonNew.setEnabled(self.selected_task is not None)
                self.pushButtonPublish.setEnabled(self.selected_task is not None)
                self.pushButtonPlayblast.setEnabled(self.selected_task is not None)
            except:
                pass

        return True        

    def search_files_dialog(self):
        dialog = SearchFilesDialog(self, self.handler, self.get_current_selection(), self.task_types)
        dialog.exec_()

    def breakout_dialog(self):
        if self.currentProject and self.currentEpisode:
            dialog = BreakoutUploadDialog(self)
            dialog.set_project(self.currentProject)
            dialog.set_episode(self.currentEpisode)
            dialog.exec_()

    def download_files(self):
        dialog = DownloadDialogGUI(self, self.get_current_selection(), self.task_types)
        dialog.resize(self.size())
        dialog.exec_()

    def load_asset(self):
        dialog = LoaderDialogGUI(self, self.handler, self.get_current_selection())

        dialog.load_files(self.tableViewFiles.model().files)
        dialog.set_selected(self.selected_file)

        #dialog.resize(self.size())
        dialog.show()

    def publish_scene(self):
        if self.selected_task:        
            dialog = PublishDialogGUI(self, self.handler, self.selected_task)
            dialog.resize(self.size())
            dialog.show()

    def playblast_scene(self):
        dialog = ZurbriggPlayblastUi()
        dialog.show()
        
        '''
        # call maya handler: import into existing workspace
        if self.handler:
            self.append_status("Running handlers")
            try:
                if (self.handler.on_playblast(source = file_name, working_dir = working_dir)):
                    self.append_status("Playblast done")
                else:
                    self.append_status("Playblast error", True)
            except:
                traceback.print_exc(file=sys.stdout)          
        else:
            self.append_status("Maya handler not loaded")


        self.append_status("{}".format(message))        
        '''


    def new_scene(self):
        if self.selected_task:
            dialog = CreateDialogGUI(self, self.handler, self.selected_task)
            dialog.show() 

'''
    ConnectionDialog class
    ################################################################################
'''

class ConnectionDialogGUI(QtWidgets.QDialog, Ui_ConnectionDialog):

    def __init__(self, parent = None):
        super(ConnectionDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.buttonBox.accepted.connect(self.save_settings)

        self.lineEditProjectsFolder.setText(load_settings("projects_root", os.path.expanduser("~")))

        self.toolButtonProjectsFolder.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonProjectsFolder.clicked.connect(self.select_projects_dir)    

        self.lineEditFfmpegBin.setText(load_settings("ffmpeg_bin", ""))

        self.toolButtonFfmpegBin.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonFfmpegBin.clicked.connect(self.select_ffmpeg_bin)    


    def select_projects_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if directory:
            self.lineEditProjectsFolder.setText(directory)

    def select_ffmpeg_bin(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select ffmpeg binary')
        if binary:
            self.lineEditFfmpegBin.setText(binary[0])            

    def save_settings(self):
        self.buttonBox.accepted.disconnect()

        save_settings('server', self.lineEditServer.text())
        save_settings('user', self.lineEditEmail.text())
        save_settings("projects_root", self.lineEditProjectsFolder.text())                            
        save_settings("ffmpeg_bin", self.lineEditFfmpegBin.text())    
        keyring.set_password('swing', 'password', self.lineEditPassword.text())

        self.buttonBox.accepted.connect(self.save_settings)
        return True

'''
    CreeateDialog class
    ################################################################################
'''

class CreateDialogGUI(QtWidgets.QDialog, Ui_CreateDialog):

    def __init__(self, parent = None, handler = None, task = None):
        super(CreateDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler

        self.shot = None
        self.asset = None
        self.url = None
        self.task = task
        self.threadpool = QtCore.QThreadPool.globalInstance()

        loader = bg.EntityLoaderThread(self, self.task["entity_id"])
        loader.callback.loaded.connect(self.entity_loaded)
        self.threadpool.start(loader)

        loader = bg.TaskFileInfoThread(self, self.task, load_settings("projects_root", os.path.expanduser("~")))
        loader.callback.loaded.connect(self.task_loaded)
        self.threadpool.start(loader)

        loader = bg.SoftwareLoader(self)            
        loader.callback.loaded.connect(self.software_loaded)
        self.threadpool.start(loader)

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonImport.clicked.connect(self.process)

        self.setWorkingDir(load_settings("projects_root", os.path.expanduser("~")))

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')        

    def software_loaded(self, results):
        self.software = results["software"]

        index = 0
        selected = 0
        for item in self.software:
            if "maya" in item["name"].lower():
                selected = index
            self.comboBoxSoftware.addItem(item["name"])
            index += 1
        self.comboBoxSoftware.setCurrentIndex(selected)

    def entity_loaded(self, data):
        self.entity = data["entity"]
        self.type = self.entity["type"]
        self.shot = None
        self.asset = None
        self.project = data["project"]

        self.project_name = self.project["name"]
        self.episode_name = None
        self.sequence_name = None
        self.shot_name = None
        self.asset_name = None
        self.task_type_name = None
        self.asset_type_name = None

        sections = []
        if self.type == "Shot":
            self.setWindowTitle("swing: create new shot")
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

            if "task_type" in self.task:
                self.task_type_name = self.task["task_type"]["name"]
                sections.append(self.task_type_name)

            self.lineEditEntity.setText(friendly_string("_".join(sections).lower()))
            self.textEditShotInfo.setText(self.shot["description"])
            self.lineEditFrameIn.setText(self.shot["frame_in"])
            self.lineEditFrameIn.setEnabled(False)
            self.lineEditFrameOut.setText(self.shot["frame_out"])
            self.lineEditFrameOut.setEnabled(False)            

            if self.shot["nb_frames"] and self.shot["nb_frames"] > 0:
                text = "{}".format(self.shot["nb_frames"])
            else:
                text = ""

            self.lineEditFrameCount.setText(text)                
            self.lineEditFrameCount.setEnabled(False)                          
        else:
            self.setWindowTitle("swing: create new asset")
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

            if "task_type" in self.task:
                self.task_type_name = self.task["task_type"]["name"]
                sections.append(self.task_type_name)          

            self.lineEditEntity.setText(friendly_string("_".join(sections).lower()))
            self.textEditShotInfo.setText(self.asset["description"].strip())
            self.lineEditFrameIn.setText("")
            self.lineEditFrameIn.setEnabled(False)
            self.lineEditFrameOut.setText("")
            self.lineEditFrameOut.setEnabled(False)
            self.lineEditFrameCount.setText("")
            self.lineEditFrameCount.setEnabled(False)         

        self.toolButtonWeb.setEnabled(self.url is not None)
        self.setEnabled(True)

    def task_loaded(self, results):
        self.task_dir = results["task_dir"]
        self.task = results["task"]

    def set_selected(self, file_item):
        index = 0
        while index < len(self.files):
            if file_item["id"] == self.files[index]["id"]:
                self.comboBoxWorkingFile.setCurrentIndex(index)
                break
            index += 1

    def setWorkingDir(self, working_dir):

        self.working_dir = working_dir
        self.lineEditWorkingDir.setText(self.working_dir)

    def close_dialog(self):
        self.close()

    def select_wcd(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if (q and q[0] != ''): 
            self.working_dir = q[0]
            self.lineEditWorkingDir.setText(self.working_dir)

    def append_status(self, status_message, error = None):
        cursor = QtGui.QTextCursor(self.textEditStatus.document()) 

        if error:       
            text = "<span style=' font-weight:100; color:#ff0000;'>{}</span><br/><br/>".format(status_message.strip())
        else:
            text = "<span style=' font-weight:100; '>{}</span><br/><bt/>".format(status_message.strip())

        cursor.insertHtml(text)

    def set_ui_enabled(self, status):
        self.lineEditEntity.setEnabled(status)
        self.lineEditFrameIn.setEnabled(status)
        self.lineEditFrameOut.setEnabled(status)
        self.lineEditWorkingDir.setEnabled(status)
        self.toolButtonWorkingDir.setEnabled(status)

        self.pushButtonImport.setEnabled(status)
        self.pushButtonCancel.setEnabled(status)

    def process(self):
        self.append_status("Creating new scene")

        mode = "working"
        software = self.software[self.comboBoxSoftware.currentIndex()]
        name = "{}{}".format(self.lineEditEntity.text().strip(), software["file_extension"])
        workingDir = self.lineEditWorkingDir.text().strip()

        workingDir = os.path.normpath(workingDir)
        workingDir = self.task_dir.replace("/mnt/content/productions", workingDir)
        workingDir = workingDir.replace("\\", "/")

        # only create working files on uploads
        # working_file = gazu.files.new_working_file(self.task, name = name, mode = mode, software = software)

        # call maya handler
        if self.handler:
            try:
                self.append_status("Create new project: {} {} {}".format(name, workingDir, software['name']))

                if (self.handler.on_create(source = name, working_dir = workingDir, software = software)):
                    self.append_status("created scene")
                else:
                    self.append_status("Error creating scene", True)

                if self.type == "Shot":
                    self.handler.set_globals(project = self.project_name, episode = self.episode_name, sequence = self.sequence_name, task = self.task_type_name, shot = self.shot_name, frame_in = self.lineEditFrameIn.text(), frame_out = self.lineEditFrameOut.text(), frame_count = self.lineEditFrameCount.text())
                else:
                    self.handler.set_globals(project = self.project_name, asset_type = self.asset_type_name, task = self.task_type_name, asset = self.asset_name)

                self.append_status("Set globals")
            except:
                traceback.print_exc(file=sys.stdout)          
        else:
            self.append_status("Maya handler not loaded")

        self.close()
    # process

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

    def __init__(self, parent = None, handler = None, task = None):
        super(UploadMonitorDialog, self).__init__(parent) # Call the inherited classes __init__ method    
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(640)

        self.model = UploadListModel(self.listView)
        self.listView.setModel(self.model)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        
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

    def add_item(self, source, text):
        self.model.add_item(source, text)         

    def reset_progressbar(self):
        self.progressBar.setRange(0, len(self.model.files))      
        self.progressBar.setValue(1)
        print("Upload monitor created for {0} files".format(len(self.model.files)))    
'''
    PublishDialogClass class
    ################################################################################
'''

class PublishDialogGUI(QtWidgets.QDialog, Ui_PublishDialog):

    def __init__(self, parent = None, handler = None, task = None):
        super(PublishDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method    

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler
        self.task = task
        self.last_dir = None
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.references = []

        name = '{}'.format(self.task["project_name"])
        name = '{} {}'.format(name, self.task["entity_type_name"])
        name = '{} {}'.format(name, self.task["entity_name"])
        name = '{} {}'.format(name, self.task["task_type_name"])        

        self.lineEditTask.setText(name)

        self.projectFileToolButton.clicked.connect(self.select_project_file)
        self.fbxFileToolButton.clicked.connect(self.select_fbx_file)
        self.reviewFileToolButton.clicked.connect(self.select_review_file)
        self.referencesAddPushButton.clicked.connect(self.select_references)

        model = QtGui.QStandardItemModel(self.referencesListView)
        self.referencesListView.setModel(model)        

        #self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        #self.toolButtonWeb.clicked.connect(self.open_url)
        #self.toolButtonWeb.setEnabled(False)

        self.pushButtonOK.clicked.connect(self.process)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        if self.handler:
            self.request = self.handler.on_save() 
            self.projectFileEdit.setText(self.request["file_path"])

    def close_dialog(self):
        self.close()

    def file_loaded(self, status):
        self.process_count -= 1
        if self.process_count == 0:
            QtWidgets.QMessageBox.question(self, 'Publishing complete', 'All files uploaded, thank you', QtWidgets.QMessageBox.Ok)
            self.pushButtonCancel.setEnabled(True)

    def process(self):
        self.pushButtonCancel.setEnabled(False)
        self.process_count = 0

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')        

        server = load_settings('server', 'https://production.wildchildanimation.com')
        edit_api = "{}/edit".format(server)        

        #self, parent, task, source, software_name, comment, email, password
        dialog = UploadMonitorDialog(self)

        # project file
        if len(self.projectFileEdit.text()) > 0:
            source = self.projectFileEdit.text()

            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)                

                worker = bg.WorkingFileUploader(self, edit_api, self.task, source, file_name, "Maya 2020", self.commentEdit.toPlainText().strip(), email, password)
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")

                self.process_count += 1                
                self.threadpool.start(worker)


        if len(self.fbxFileEdit.text()) > 0:
            source = self.fbxFileEdit.text()
            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)

                worker = bg.WorkingFileUploader(self, edit_api, self.task, source, file_name, "fbx", self.commentEdit.toPlainText().strip(), email, password)
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")    

                self.process_count += 1
                self.threadpool.start(worker)            

        if len(self.reviewFileEdit.text()) > 0:
            source = self.reviewFileEdit.text()
            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)

                worker = bg.WorkingFileUploader(self, edit_api, self.task, source, file_name, "wip", self.commentEdit.toPlainText().strip(), email, password, mode = "preview")
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")    

                self.process_count += 1
                self.threadpool.start(worker)   

        row = 0
        model = self.referencesListView.model()
        while row < model.rowCount():
            item = model.item(row)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                source = model.data(item.index())

                if os.path.exists(source):
                    file_base = os.path.basename(source)
                    file_path = os.path.dirname(source)
                    file_name, file_ext = os.path.splitext(file_base)

                    worker = bg.WorkingFileUploader(self, edit_api, self.task, source, file_name, "working", self.commentEdit.toPlainText().strip(), email, password)
                    worker.callback.progress.connect(dialog.file_loading)
                    worker.callback.done.connect(dialog.file_loaded)
                    dialog.add_item(source, "Pending")   

                    self.process_count += 1
                    self.threadpool.start(worker)                  
            row += 1

        dialog.reset_progressbar()
        dialog.show()
        self.hide()

    def get_references(self):
        return self.references

    def select_references(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."
        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileNames(self, "Add secondary assets", self.last_dir, "All Files (*.*)")
        if not (q):
            return 

        for name in q[0]:
            self.references.append(name)

        model = QtGui.QStandardItemModel(self.referencesListView)
        for item in self.references:
            list_item = QtGui.QStandardItem(item)
            list_item.setCheckable(True)
            list_item.setCheckState(QtCore.Qt.CheckState.Checked)
            model.appendRow(list_item)

        self.referencesListView.setModel(model)

    def select_project_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."
        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Project File", self.last_dir, "Maya Ascii (*.ma), Maya Binary (*.mb), All Files (*.*)")
        if (q and q[0] != ''):        
            self.projectFileEdit.setText(q[0])
            self.last_dir = q[0]

    def select_fbx_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."
        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Output File", self.last_dir, "FBX (*.fbx), All Files (*.*)")
        if (q and q[0] != ''):     
            self.fbxFileEdit.setText(q[0])
            self.last_dir = q[0]

    def select_review_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."

        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Review File", self.last_dir, "Images (*.bmp, *.jpg, *.png), Videos (*.mp4), All Files (*.*)")
        if (q and q[0] != ''):     
            self.reviewFileEdit.setText(q[0])

            source = self.reviewFileEdit.text()
            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)

                self.reviewTitleLineEdit.setText(file_name)
                self.last_dir = q[0]

'''
    LoaderDialog class
    ################################################################################
'''

class LoaderDialogGUI(QtWidgets.QDialog, Ui_LoaderDialog):

    def __init__(self, parent = None, handler = None, entity = None):
        super(LoaderDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler
        self.entity = entity
        self.shot = None
        self.asset = None
        self.url = None
        self.threadpool = QtCore.QThreadPool.globalInstance()

        loader = bg.EntityLoaderThread(self, self.entity["id"])
        loader.callback.loaded.connect(self.entity_loaded)
        self.threadpool.start(loader)

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonImport.clicked.connect(self.process)

        self.setWorkingDir(load_settings("projects_root", os.path.expanduser("~")))

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')        

    def entity_loaded(self, data):
        self.type = data["type"]
        self.project = data["project"]

        self.shot = None
        self.asset = None

        self.project_name = None
        self.episode_name = None
        self.sequence_name = None
        self.shot_name = None
        self.asset_name = None
        self.task_type_name = None
        self.asset_type_name = None

        sections = []
        if self.type == "Shot":
            self.setWindowTitle("swing: import shot")
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

            #if "task_type" in self.task:
            #    self.task_type_name = self.task["task_type"]["name"]
            #    sections.append(self.task_type_name)

            self.lineEditEntity.setText(" / ".join(sections))

            self.textEditShotInfo.setText(self.shot["description"])

            self.lineEditFrameIn.setText(self.shot["frame_in"])
            self.lineEditFrameIn.setEnabled(False)

            self.lineEditFrameOut.setText(self.shot["frame_out"])
            self.lineEditFrameOut.setEnabled(False)            

            if self.shot["nb_frames"] and len(self.shot["nb_frames"] > 0):
                self.lineEditFrameCount.setText()
            else:
                text = ""
            self.lineEditFrameCount.setText(text)                
            self.lineEditFrameCount.setEnabled(False)                          
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

            #if "task_type" in self.task:
            #    self.task_type_name = self.task["task_type"]["name"]
            #    sections.append(self.task_type_name)               

            sections.append(self.entity["name"].strip())

            self.lineEditEntity.setText(" / ".join(sections))
            self.textEditShotInfo.setText(self.asset["description"].strip())

            self.lineEditFrameIn.setText("")
            self.lineEditFrameIn.setEnabled(False)

            self.lineEditFrameOut.setText("")
            self.lineEditFrameOut.setEnabled(False)

            self.lineEditFrameCount.setText("")
            self.lineEditFrameCount.setEnabled(False)

        namespace = "_".join(sections).lower().strip()
        #if self.asset_type_name:
        #    namespace = self.asset_type_name
        #elif self.asset_name:
        #    namespace = self.asset_name
        #elif self.task_type_name:
        #    namespace = self.task_type_name
        #elif self.shot_name:
        #    namespace = self.shot_name
        #else:
        #    namespace = "_ns"

        self.lineEditNamespace.setText(namespace)
        self.toolButtonWeb.setEnabled(self.url is not None)
        self.setEnabled(True)

    def load_files(self, file_list, selected_file = None):
        index = 0
        selected_index = 0

        self.files = file_list
        self.comboBoxWorkingFile.clear()
        for item in self.files:
            self.comboBoxWorkingFile.addItem(item["name"])
            if selected_file and selected_file == item:
                selected_index = index
            index += 1

        if selected_file:
            self.comboBoxWorkingFile.setCurrentIndex(selected_index)

    def set_selected(self, file_item):
        index = 0
        while index < len(self.files):
            if file_item["id"] == self.files[index]["id"]:
                self.comboBoxWorkingFile.setCurrentIndex(index)
                break
            index += 1

    def setWorkingDir(self, working_dir):
        self.working_dir = working_dir
        self.lineEditWorkingDir.setText(self.working_dir)

    def close_dialog(self):
        self.close()

    def select_wcd(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if (q):
            self.setWorkingDir(q[0][1])

    def append_status(self, status_message, error = None):
        cursor = QtGui.QTextCursor(self.textEditStatus.document()) 

        if error:       
            text = "<span style=' font-weight:100; color:#ff0000;'>{}</span><br/><br/>".format(status_message.strip())
        else:
            text = "<span style=' font-weight:100; '>{}</span><br/><bt/>".format(status_message.strip())

        cursor.insertHtml(text)

    def file_loaded(self, results):
        status = results["status"]
        message = results["message"]
        size = results["size"]
        row = results["file_id"]
        file_name = results["target"]
        working_dir = results["working_dir"]
        self.append_status(message, "error" in status)

        # call maya handler: import into existing workspace
        if self.handler:
            try:
                if self.checkBoxReferences.checkState() == QtCore.Qt.Checked:
                    # see if we know a namespace
                    if self.checkBoxNamespace.checkState() == QtCore.Qt.Checked:
                        namespace = self.lineEditNamespace.text()
                    else:
                        namespace = None

                    self.append_status("Importing reference {}".format(file_name))
                    if (self.handler.import_reference(source = file_name, working_dir = working_dir, namespace = namespace)):
                        self.append_status("Import done")
                    else:
                        self.append_status("Import error", True)
                else:
                    self.append_status("Loading file {}".format(file_name))
                    if (self.handler.load_file(source = file_name, working_dir = working_dir)):
                        self.append_status("Loading done")
                    else:
                        self.append_status("Loading error", True)

            except:
                traceback.print_exc(file=sys.stdout)          
        else:
            self.append_status("Maya handler not loaded")

        self.append_status("{}".format(message))
        self.set_ui_enabled(True)

    def file_loading(self, result):
        message = result["message"]
        size = result["size"]
        row = result["file_id"]
        file_name = result["target"]

        self.append_status("{} {}".format(message, human_size(size)))

    def set_ui_enabled(self, status):
        self.comboBoxWorkingFile.setEnabled(status)
        self.lineEditEntity.setEnabled(status)
        self.lineEditFrameIn.setEnabled(status)
        self.lineEditFrameOut.setEnabled(status)
        self.lineEditWorkingDir.setEnabled(status)
        self.toolButtonWorkingDir.setEnabled(status)
        self.checkBoxSkipExisting.setEnabled(status)

        self.checkBoxSkipExisting.setEnabled(status)
        self.checkBoxExtractZips.setEnabled(status)
        self.pushButtonImport.setEnabled(status)
        self.pushButtonCancel.setEnabled(status)

    def process(self):
        #self.threadpool = QtCore.QThreadPool()
        self.textEditStatus.clear()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.set_ui_enabled(False)
        self.process_count = 0

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://production.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        # download the currently selected file
        item = self.files[self.comboBoxWorkingFile.currentIndex()]
        row = 0
        if "WorkingFile" in item["type"]:
            #target = os.path.normpath(os.path.join(self.working_dir, item["name"]))
            url = "{}/api/working_file/{}".format(edit_api, item["id"])
            target = set_target(item, self.working_dir)

            worker = bg.FileDownloader(self, self.working_dir, item["id"], url, item["target_path"], email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

            worker.callback.progress.connect(self.file_loading)
            worker.callback.done.connect(self.file_loaded)

            self.process_count += 1
            self.threadpool.start(worker)
            self.append_status("Downloading {} to {}".format(item["name"], item["target_path"]))
            #file_item["status"] = "Busy"
        else:
            #target = os.path.normpath(os.path.join(self.working_dir, item["name"]))
            url = "{}/api/output_file/{}".format(edit_api, item["id"])
            target = set_target(item, self.working_dir)

            worker = bg.FileDownloader(self, self.working_dir, item["id"], url,  item["target_path"], email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

            worker.callback.progress.connect(self.file_loading)
            worker.callback.done.connect(self.file_loaded)
            
            self.process_count += 1
            self.threadpool.start(worker)
            self.append_status("Downloading {} to {}".format(item["name"], item["target_path"]))
        # file type
    # process


