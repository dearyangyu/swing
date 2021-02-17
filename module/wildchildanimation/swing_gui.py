# -*- coding: utf-8 -*-
import traceback
import sys
import os

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

from wildchildanimation.gui.main_form import Ui_WcaMayaDialog
from wildchildanimation.gui.connection_dialog import Ui_ConnectionDialog
from wildchildanimation.gui.publish_dialog import Ui_PublishDialog
from wildchildanimation.gui.download_dialog import Ui_DownloadDialog
from wildchildanimation.gui.loader_dialog import Ui_LoaderDialog

from wildchildanimation.gui.swing_tables import FileTableModel, TaskTableModel, CastingTableModel, load_file_table_widget, human_size

import pymel

def resource_path(resource):
    base_path = os.path.dirname(os.path.realpath(__file__))
    #uic.loadUi(os.path.join(root, resource_file), self)
    #base_path = os.path.abspath(".")
    return os.path.join(base_path, resource)
### 

def my_date_format(date):
    if len(date) == 19: # YYYY-MM-DDTHH:MM:SS
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return date.strftime("%Y-%m-%d %H:%M:%S")

class SwingGUI(QtWidgets.QDialog, Ui_WcaMayaDialog):
    loading = False
    user_email = None
    tasks = []
    task_types = []

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

    def __init__(self, studio_handler = None):
        super(SwingGUI, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.handler = studio_handler

        QtCore.QCoreApplication.setOrganizationName("Wild Child Animation")
        QtCore.QCoreApplication.setOrganizationDomain("wildchildanimation.com")
        QtCore.QCoreApplication.setApplicationName("Treehouse: Swing")        
        
        self.comboBoxAsset.currentIndexChanged.connect(self.load_asset_files)
        self.comboBoxShot.currentIndexChanged.connect(self.load_shot_files)    

        self.pushButtonSettings.clicked.connect(self.open_connection_settings)
        self.pushButtonConnect.clicked.connect(self.connect_to_server)
        self.pushButtonLoad.clicked.connect(self.load_asset)
        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonPublish.clicked.connect(self.publish_scene)

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

        if self.connect_to_server():
            self.labelConnection.setText("Connected")
            self.refresh_data()


    def open_file_item(self, index):
        item = self.treeWidgetFiles.itemFromIndex(index)

        if not item:
            return False

        file_name = item.data(index.row(), 0)
        
        working_dir = load_settings("working_dir", os.path.expanduser("~"))
        file_item = os.path.join(os.path.join(file_name, working_dir))

        file_list = self.get_file_selection_list()

        dialog = LoaderDialogGUI(self)
        dialog.load_files(file_list)
        dialog.set_file_name(file_name)
        dialog.exec_()        

    def set_loading(self, is_loading):
        self.loading = is_loading

        if self.loading:
            self.labelMessage.setText("Loading ...")
        else:
            self.labelMessage.setText("OK")

        #self.comboBoxProject.setEnabled(not is_loading)
        self.comboBoxEpisode.setEnabled(not is_loading)
        self.comboBoxSequence.setEnabled(not is_loading)
        self.comboBoxShot.setEnabled(not is_loading)
        self.comboBoxAssetType.setEnabled(not is_loading)
        self.radioButtonAsset.setEnabled(not is_loading)
        self.radioButtonShot.setEnabled(not is_loading)
        self.tabWidget.setEnabled(not is_loading)

        #self.pushButtonLoad.setEnabled(not is_loading)
        #self.pushButtonImport.setEnabled(not is_loading)
        #self.pushButtonDownload.setEnabled(not is_loading)
        #self.pushButtonPublish.setEnabled(not is_loading)

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
                    asset_loader.loaded.connect(self.asset_types_loaded)
                    asset_loader.start()

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
        print("loading settings")

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
        print("[refresh_data]")

        if not self.loading:
            self.comboBoxProject.blockSignals(True)
            loader = bg.ProjectLoaderThread(self)
            loader.loaded.connect(self.projects_loaded)

            self.labelMessage.setText("Loading ...")
            self.set_loading(True)
            loader.start()
        else:
            print("Loading in progress")

    def projects_loaded(self, results): 
        print("[projects_loaded]")
        #self.comboBoxProject.setEnabled(True)

        self.labelMessage.setText("OK")
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

    def project_changed(self, index):
        print("[project_changed]")

        self.currentProject = self.projects[index]
        self.currentProjectIndex = index

        self.comboBoxEpisode.clear()
        self.comboBoxSequence.clear()
        self.comboBoxShot.clear()
        self.comboBoxAssetType.clear()

        if self.currentProject:
            self.labelMessage.setText("Loading ...")
            self.set_loading(True)                

            loader = bg.ProjectHierarchyLoaderThread(self, self.currentProject)
            loader.loaded.connect(self.hierarchy_loaded)
            loader.start()

            asset_loader = bg.AssetTypeLoaderThread(self, self.currentProject)
            asset_loader.loaded.connect(self.asset_types_loaded)
            asset_loader.start()

            task_loader = bg.TaskLoaderThread(self, self.currentProject, self.user_email)
            task_loader.loaded.connect(self.tasks_loaded)
            task_loader.start()            


    def hierarchy_loaded(self, data): 
        print("[hierarchy_loaded]")
        self.labelMessage.setText("OK")
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
        print("[episode_changed]")
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
        
        self.labelMessage.setText("OK")

    def asset_types_loaded(self, data): 
        print("[asset_types_loaded]")
        self.asset_types = data

        self.comboBoxAssetType.blockSignals(True)
        self.comboBoxAssetType.clear()
        for item in self.asset_types:
            name = "{} {}".format(self.currentProject["code"], item["name"])            
            self.comboBoxAssetType.addItem(name) 
        self.comboBoxAssetType.blockSignals(False)                       
        self.comboBoxAssetType.setEnabled(True)

        if len(self.asset_types) > 0:
            self.asset_type_changed(0)

    def tasks_loaded(self, data):
        print("[tasks_loaded]")

        self.tasks = data
        self.load_tasks(self.tasks)

    def sequence_changed(self, index):
        print("[sequence_changed]")

        self.currentSequencesIndex = self.comboBoxSequence.currentIndex()
        self.currentSequences = self.currentEpisode["sequences"]
        self.currentEpisode["sequences"][self.currentSequencesIndex]

        self.comboBoxShot.blockSignals(True)                 
        self.comboBoxShot.clear()

        for item in self.currentSequences[self.currentSequencesIndex]["shots"]:
            name = "{} {}".format(item["sequence_name"],  item["name"])
            self.comboBoxShot.addItem(name) 
        self.comboBoxShot.blockSignals(False)                 

        if len(self.currentSequences[self.currentSequencesIndex]["shots"]) > 0:
            if self.radioButtonShot.isChecked():
                self.comboBoxShot.setEnabled(True)
                self.load_shot_files(0)

    def asset_type_changed(self, index):
        print("[asset_type_changed]")
        self.currentAssetType = self.asset_types[index]

        loader = bg.AssetLoaderThread(self, self.currentProject, self.currentAssetType)
        loader.loaded.connect(self.asset_loaded)
        loader.start()

    def load_shot_files(self, index):
        self.currentShot = self.currentSequences[self.currentSequencesIndex]["shots"][index]
        print("load shot files {}".format(index))

        loader = bg.EntityFileLoader(self, self.currentShot)
        loader.loaded.connect(self.files_loaded)
        loader.start()

    def files_loaded(self, data):
        output_files = data["output_files"]
        working_files = data["working_files"]

        self.load_files(output_files, working_files)        
        print("Loaded {} output files, {} working files".format(len(output_files), len(working_files)))

    def asset_loaded(self, data): 
        print("[asset_loaded]")

        self.assets = data
        self.comboBoxAsset.clear()

        last = self.comboBoxAsset.currentIndex()
        for p in self.assets:
            name = ""

            if self.currentProject:
                name = "{} {}".format(name, self.currentProject["code"])

            if self.currentEpisode:
                name = "{} {}".format(name, self.currentEpisode["name"])

            if self.currentSequences and self.currentSequencesIndex and len(self.currentSequences) > 0:
                name = "{} {}".format(name, self.currentSequences[self.currentSequencesIndex]["name"])

            name = "{} {}".format(name, p["name"]).strip()
            self.comboBoxAsset.addItem(name)     
        self.comboBoxAsset.setEnabled(True)       

    def load_asset_files(self, index):
        self.currentAsset = self.assets[index]

        print("load asset files {}".format(index))
        loader = bg.EntityFileLoader(self, self.currentAsset)
        loader.loaded.connect(self.files_loaded)
        loader.start()        

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
        self.tableViewFiles.setColumnWidth(0, 400)
        self.tableViewFiles.setColumnWidth(1, 100)
        self.tableViewFiles.setColumnWidth(2, 75)
        self.tableViewFiles.setColumnWidth(3, 200)
        self.tableViewFiles.setColumnWidth(4, 350)
        self.tableViewFiles.setColumnWidth(6, 200)

        selectionModel = self.tableViewFiles.selectionModel()
        selectionModel.selectionChanged.connect(self.file_table_selection_changed)       

        self.pushButtonDownload.setEnabled(len(self.files) > 0)    

    def file_table_double_click(self, index):
        row_index = index.row()
        self.selected_file = self.tableViewFiles.model().files[row_index]
        if self.selected_file:
            dialog = LoaderDialogGUI(self, self.handler, self.get_current_selection())
            dialog.load_files(self.tableViewFiles.model().files)
            dialog.set_selected(self.selected_file)
            dialog.exec_()


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
        self.tableViewTasks.setModel(TaskTableModel(self, tasks))
        self.tableViewTasks.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableViewTasks.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableViewTasks.setColumnWidth(0, 400)
        self.tableViewTasks.setColumnWidth(1, 100)
        self.tableViewTasks.setColumnWidth(2, 75)

        self.pushButtonPublish.setEnabled(len(tasks) > 0)

    def download_files(self):
        dialog = DownloadDialogGUI(self, self.get_current_selection())
        dialog.load_files(self.tableViewFiles.model().files)
        dialog.set_selected(self.selected_file)
        dialog.resize(self.size())
        dialog.exec_()

    def load_asset(self):
        dialog = LoaderDialogGUI(self)
        #dialog.resize(self.size())
        dialog.exec_()

    def publish_scene(self):
        dialog = PublishDialogGUI(self, self.listWidgetTasks.currentItem().data(QtCore.Qt.UserRole))
        dialog.resize(self.size())
        dialog.exec_()

class ConnectionDialogGUI(QtWidgets.QDialog, Ui_ConnectionDialog):

    def __init__(self, parent = None):
        super(ConnectionDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)

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

class PublishDialogGUI(QtWidgets.QDialog, Ui_PublishDialog):

    def __init__(self, parent = None, item = None):
        super(PublishDialogGUI, self).__init__() # Call the inherited classes __init__ method
        self.setupUi(self)

        self.task = item["task"]
        self.last_dir = None

        #resource_file = "gui/forms/maya/publish_dialog.ui"
        #uic.loadUi(resource_path(resource_file), self)

        name = '{}'.format(self.task["project_name"])
        name = '{} {}'.format(name, self.task["entity_type_name"])
        name = '{} {}'.format(name, self.task["entity_name"])
        name = '{} {}'.format(name, self.task["task_type_name"])        

        self.lineEditTask.setText(name)

        self.projectFileToolButton.clicked.connect(self.select_project_file)
        self.fbxFileToolButton.clicked.connect(self.select_fbx_file)
        self.reviewFileToolButton.clicked.connect(self.select_review_file)

        self.pushButtonOK.clicked.connect(self.accept)
        self.pushButtonCancel.clicked.connect(self.close_dialog)        

    def close_dialog(self):
        self.close()

    def get_references(self):
        return []

    def select_project_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."
        
        #Get the file location
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Open Project File", self.last_dir, "C4d (*.c4d), All Files (*.*)")
        if (file):
            self.projectFileEdit.setText(file[0])
            self.last_dir = file[0]

    def select_fbx_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."

        
        #Get the file location
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Open Output File", self.last_dir, "FBX (*.fbx), All Files (*.*)")
        if (file):
            self.fbxFileEdit.setText(file[0])
            self.last_dir = file[0]

    def select_review_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."

        
        #Get the file location
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Open Review File", self.last_dir, "Images (*.bmp, *.jpg, *.png), Videos (*.mp4), All Files (*.*)")
        if (file):
            self.reviewFileEdit.setText(file[0])
            self.reviewTitleLineEdit.setText(file[0])
            self.last_dir = file[0]

class LoaderDialogGUI(QtWidgets.QDialog, Ui_LoaderDialog):

    def __init__(self, parent = None, handler = None, entity = None):
        super(LoaderDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.handler = handler
        self.entity = entity
        self.shot = None
        self.asset = None
        self.url = None

        if self.entity:
            loader = bg.EntityLoaderThread(self, self.entity["type"], self.entity["id"])
            loader.loaded.connect(self.entity_loaded)
            loader.start()

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonImport.clicked.connect(self.process)

        self.setWorkingDir(load_settings("working_dir", os.path.expanduser("~")))

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')        

    def entity_loaded(self, data):
        self.shot = None
        self.asset = None
        self.project = data["project"]

        sections = []
        if self.entity["type"] == "Shot":
            self.shot = data["item"]
            self.url = data["url"]
            self.labelEntity.setText("Shot")

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

            self.textEditShotInfo.setText(self.shot["description"])

            self.lineEditFrameIn.setText(self.shot["frame_in"])
            self.lineEditFrameIn.setEnabled(False)

            self.lineEditFrameOut.setText(self.shot["frame_out"])
            self.lineEditFrameOut.setEnabled(False)            

            self.lineEditFrameCount.setText(self.shot["nb_frames"])
            self.lineEditFrameCount.setEnabled(False)                          

            working_dir = "{}{}{}".format(self.working_dir, os.path.sep, "/".join(sections))
            self.setWorkingDir(os.path.normpath(working_dir))
        else:
            self.asset = data["item"]
            self.url = data["url"]
            self.labelEntity.setText("Asset")

            if "code" in self.project:
                sections.append(self.project["code"])
            else:
                sections.append(self.project["name"])            
            sections.append("assets")

            if "asset_type_name" in self.asset:
                sections.append(self.asset["asset_type_name"].strip())                 

            sections.append(self.entity["name"].strip())

            self.lineEditEntity.setText(" / ".join(sections))

            self.textEditShotInfo.setText(self.asset["description"].strip())

            self.lineEditFrameIn.setText("")
            self.lineEditFrameIn.setEnabled(False)

            self.lineEditFrameOut.setText("")
            self.lineEditFrameOut.setEnabled(False)

            self.lineEditFrameCount.setText("")
            self.lineEditFrameCount.setEnabled(False)

            working_dir = "{}{}{}".format(self.working_dir, os.path.sep, "/".join(sections))
            self.setWorkingDir(os.path.normpath(working_dir))           

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
        self.working_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')

        self.lineEditWorkingDir.setText(self.working_dir)
        save_settings("working_dir", self.working_dir)

    def append_status(self, status_message, error = None):
        cursor = QtGui.QTextCursor(self.textEditStatus.document()) 

        if error:       
            text = "<span style=' font-weight:100; color:#ff0000;'>{}</span><br/><br/>".format(status_message.strip())
        else:
            text = "<span style=' font-weight:100; '>{}</span><br/><bt/>".format(status_message.strip())

        cursor.insertHtml(text)

    def file_loaded(self, results):
        message = results["message"]
        size = results["size"]
        row = results["file_id"]
        file_name = results["target"]
        working_dir = results["working_dir"]

        if self.handler:
            self.append_status("Running handlers")
            try:
                self.handler.on_import_file(file_name, working_dir)
                self.append_status("Handlers done")
            except:
                traceback.print_exc(file=sys.stdout)          

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
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://production.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        # download the currently selected file
        item = self.files[self.comboBoxWorkingFile.currentIndex()]
        row = 0
        print("Downloading {} to {}".format(item["name"], self.working_dir))
        if "working_file" in item["type"]:
            target = os.path.normpath(os.path.join(self.working_dir, item["name"]))
            url = "{}/api/working_file/{}".format(edit_api, item["id"])

            worker = bg.FileDownloader(self, self.working_dir, item["id"], url, target, email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

            worker.callback.progress.connect(self.file_loading)
            worker.callback.done.connect(self.file_loaded)

            self.threadpool.start(worker)
            self.append_status("Loading {}".format(item["name"]))
            #file_item["status"] = "Busy"
        else:
            target = os.path.normpath(os.path.join(self.working_dir, item["name"]))
            url = "{}/api/output_file/{}".format(edit_api, item["id"])

            worker = bg.FileDownloader(self, self.working_dir, item["id"], url, target, email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

            worker.callback.progress.connect(self.file_loading)
            worker.callback.done.connect(self.file_loaded)
            
            self.threadpool.start(worker)
            self.append_status("Loading {}".format(item["name"]))
        # file type
    # process

class DownloadDialogGUI(QtWidgets.QDialog, Ui_DownloadDialog):

    working_dir = None
    
    def __init__(self, parent = None, entity = None):
        super(DownloadDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.entity = entity 

        if self.entity:
            loader = bg.EntityLoaderThread(self, self.entity["type"], self.entity["id"])
            loader.loaded.connect(self.entity_loaded)
            loader.start()     

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)               

        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        self.setWorkingDir(load_settings("working_dir", os.path.expanduser("~")))

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')              

    def entity_loaded(self, data):
        self.shot = None
        self.asset = None
        self.project = data["project"]

        sections = []
        if self.entity["type"] == "Shot":
            self.shot = data["item"]
            self.url = data["url"]
            self.labelEntity.setText("Shot")

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

            working_dir = "{}{}{}".format(self.working_dir, os.path.sep, "/".join(sections))
            self.setWorkingDir(os.path.normpath(working_dir))
        else:
            self.asset = data["item"]
            self.url = data["url"]
            self.labelEntity.setText("Asset")

            if "code" in self.project:
                sections.append(self.project["code"])
            else:
                sections.append(self.project["name"])            
            sections.append("assets")

            if "asset_type_name" in self.asset:
                sections.append(self.asset["asset_type_name"].strip())                 

            sections.append(self.entity["name"].strip())

            self.lineEditEntity.setText(" / ".join(sections))

            working_dir = "{}{}{}".format(self.working_dir, os.path.sep, "/".join(sections))
            self.setWorkingDir(os.path.normpath(working_dir))           

        self.toolButtonWeb.setEnabled(self.url is not None)
        self.setEnabled(True)


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
        self.working_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        self.lineEditWorkingDirectory.setText(self.working_dir)

    def file_loaded(self, results):
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
                status_item.setText("Downloaded {}".format(human_size(size)))
                break        

            index += 1

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
                break
            index += 1        


    def load_files(self, files):
        self.files = files

        load_file_table_widget(self.tableWidget, self.files)

    def download_files(self):
        self.pushButtonDownload.blockSignals(True)
        self.threadpool = QtCore.QThreadPool()

        file_list = []

        index = 0
        while index < self.tableWidget.rowCount():
            row_item = self.tableWidget.item(index, 0)
            if row_item.checkState():
                file_list.append(row_item.data(QtCore.Qt.UserRole))

            index += 1

        print("Downloading {} files".format(len(file_list)))
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://production.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        row = 0
        for item in file_list:
            print("Downloading {} to {}".format(item["name"], self.working_dir))
            if "working_file" in item["type"]:
                target = os.path.normpath(os.path.join(self.working_dir, item["name"]))
                url = "{}/api/preview_file/{}".format(edit_api, item["id"])

                worker = bg.FileDownloader(self, self.working_dir, item["id"], url, target, email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

                worker.callback.progress.connect(self.file_loading)
                worker.callback.done.connect(self.file_loaded)

                self.threadpool.start(worker)
                item["status"] = "Busy"
            else:
                target = os.path.normpath(os.path.join(self.working_dir, item["name"]))
                url = "{}/api/output_file/{}".format(edit_api, item["id"])

                worker = bg.FileDownloader(self, self.working_dir, item["id"], url, target, email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

                worker.callback.progress.connect(self.file_loading)
                worker.callback.done.connect(self.file_loaded)
                
                self.threadpool.start(worker)
                item["status"] = "Busy"
            row = row + 1        
        self.pushButtonDownload.blockSignals(False)

def load_settings(key, default):
    settings = QtCore.QSettings()    
    return settings.value(key, default)

def save_settings(key, val):
    settings = QtCore.QSettings()    
    settings.setValue(key, val)
    settings.sync()
    return settings.value(key)    

def load_keyring(key, val, default):
    result = keyring.get_password(key, val)
    if result == None:
        keyring.set_password(key, val, default)
        result = keyring.get_password(key, val)
    return result
