# -*- coding: utf-8 -*-
# PyQt Gui plugin for Treehouse
#
# version: 1.000
# date: 18 Feb 2021
#
#############################
from genericpath import exists
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

import gazu
import os.path

from datetime import datetime

from wildchildanimation.gui.background_workers import *

from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.create_dialog import Ui_CreateDialog

from wildchildanimation.gui.loader import *
from wildchildanimation.gui.references import *
from wildchildanimation.gui.search import *
from wildchildanimation.gui.downloads import *
from wildchildanimation.gui.publish import *
from wildchildanimation.gui.playlists import *
from wildchildanimation.gui.breakout import *
from wildchildanimation.gui.entity_info import *
from wildchildanimation.gui.dcc_tools import *

from wildchildanimation.gui.swing_tables import FileTableModel, CheckBoxDelegate, TaskTableModel, setup_file_table

from wildchildanimation.gui.swing_desktop import Ui_SwingMain
from wildchildanimation.gui.project_nav import ProjectNavWidget

from wildchildanimation.studio_interface import StudioInterface

from wildchildanimation.gui.swing_playblast import *
from wildchildanimation.gui.settings import SwingSettings, SettingsDialog


'''
    SwingGUI Main class
    ################################################################################
'''
class SwingGUI(QtWidgets.QDialog, Ui_SwingMain):
    loading = False
    user_email = None
    tasks = []
    task_types = []

    first_load = True

    currentProject = None
    currentEpisode = None
    currentSequences = None
    currentSequencesIndex = None
    currentTask = None
    currentAssetType = None
    gazu_client = None
    connected = False
    project_root = None
    currentWorkingDir = None

    selected_file = None
    selected_task = None

    dlg_instance = None

    swing_settings = None

    @classmethod
    def show_dialog(cls, handler = StudioInterface()):
        if not cls.dlg_instance:
            cls.dlg_instance = SwingGUI(handler)

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()    

    def keyPressEvent(self, event):
        super(SwingGUI, self).keyPressEvent(event)            

    def __init__(self, studio_handler):
        super(SwingGUI, self).__init__(None) # Call the inherited classes __init__ method

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint ^ QtCore.Qt.WindowMinMaxButtonsHint)

        # setup to hide in a dcc
        self.set_handler(studio_handler)

        self.connect(self, QtCore.SIGNAL("finished(int)"), self.finished)
        self.setWindowTitle("{} v{}".format(SwingSettings._APP_NAME, SwingSettings._APP_VERSION))

        resource_file = resource_path("../resources/swing_logo_white_small.png")
        if os.path.exists(resource_file):
            icon = QtGui.QIcon(resource_file)
            self.setWindowIcon(icon)

        self.swing_settings = SwingSettings.getInstance()

        self.projectNav = ProjectNavWidget()
        self.projectNav.signal.selection_changed.connect(self.selection_changed)        

        self.horizontalLayoutProject.addWidget(self.projectNav)
        
        self.comboBoxAsset.currentIndexChanged.connect(self.load_asset_files)
        self.comboBoxShot.currentIndexChanged.connect(self.load_shot_files)    

        self.pushButtonSettings.clicked.connect(self.open_connection_settings)
        self.pushButtonConnect.clicked.connect(self.connect_to_server)

        self.toolButtonImport.clicked.connect(self.load_asset)
        self.toolButtonDownload.clicked.connect(self.download_files)
        self.toolButtonPublish.clicked.connect(self.publish_scene)

        self.pushButtonPlayblast.clicked.connect(self.playblast_dialog)
        self.pushButtonExport.clicked.connect(self.dcc_tools_dialog)

        self.toolButtonNew.clicked.connect(self.new_scene)
        
        self.pushButtonBreakout.clicked.connect(self.breakout_dialog)
        ##self.pushButtonPlaylists.clicked.connect(self.playlist_dialog)
        self.pushButtonSearchFiles.clicked.connect(self.search_files_dialog)

        self.projectNav.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.projectNav.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.projectNav.comboBoxSequence.currentIndexChanged.connect(self.sequence_changed)

        self.comboBoxAssetType.currentIndexChanged.connect(self.asset_type_changed)      

        self.radioButtonShot.toggled.connect(self.set_to_shot)
        self.radioButtonAsset.toggled.connect(self.set_to_asset)

        #self.treeWidgetFiles.doubleClicked.connect(self.open_file_item)
        self.tableViewFiles.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewFiles.doubleClicked.connect(self.file_table_double_click)
        self.tableViewFiles.clicked.connect(self.select_row)       

        self.tableViewTasks.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewTasks.doubleClicked.connect(self.task_table_double_click)        

        self.toolButtonShotInfo.clicked.connect(self.load_shot_info)
        set_button_icon(self.toolButtonShotInfo, "../resources/fa-free/solid/video.svg")        

        self.toolButtonAssetInfo.clicked.connect(self.load_asset_info)
        set_button_icon(self.toolButtonAssetInfo, "../resources/fa-free/solid/boxes.svg")    

        self.toolButtonFileTableSelectAll.clicked.connect(self.select_all_files)
        self.toolButtonFileSelectNone.clicked.connect(self.select_no_files)

        self.readSettings()
        self._createActions()
        self._createContextMenu()

        self.threadpool = QtCore.QThreadPool.globalInstance()

        if self.connect_to_server():
            self.labelConnection.setText("Connected")
            self.projectNav.load_open_projects()
            self.version_check()

    def select_all_files(self):
        for row in range(self.tableViewFiles.model().rowCount()):
            index = self.tableViewFiles.model().index(row, 0)
            self.tableViewFiles.model().setData(index, True, QtCore.Qt.EditRole)
        self.tableViewFiles.update()

    def select_no_files(self):
        for row in range(self.tableViewFiles.model().rowCount()):
            index = self.tableViewFiles.model().index(row, 0)
            self.tableViewFiles.model().setData(index, False, QtCore.Qt.EditRole)
        self.tableViewFiles.update()    

    def _loadActionIcon(self,  action_text, resource_string):
        action = QtWidgets.QAction(self)
        action.setText(action_text)

        resource_file = resource_path(resource_string)
        if os.path.exists(resource_file):
            pm = QtGui.QPixmap(resource_file)
            pm = pm.scaledToHeight(14)

            icon = QtGui.QIcon(pm)            
            action.setIcon(icon)

        return action

    def _createActions(self):
        # File actions
        self.filesSelectAllAction = self._loadActionIcon("&Select All", "../resources/fa-free/solid/plus.svg")
        self.filesSelectAllAction.setStatusTip("Select all")
        self.filesSelectAllAction.triggered.connect(self.select_all_files)

        self.filesSelectNoneAction = self._loadActionIcon("&Select None", "../resources/fa-free/solid/minus.svg")
        self.filesSelectNoneAction.setStatusTip("Select none")
        self.filesSelectNoneAction.triggered.connect(self.select_no_files)

        #self.filesImportAction = self._loadActionIcon("&Import Files", "../resources/fa-free/solid/download.svg")
        #self.filesImportAction.setStatusTip("Open Loader")
        #self.filesImportAction.triggered.connect(self.load_asset)

        #self.filesDownloadAction = self._loadActionIcon("&Download Files", "../resources/fa-free/solid/download.svg")
        #self.filesDownloadAction.setStatusTip("Open Downloader")
        #self.filesDownloadAction.triggered.connect(self.download_files)   

        #self.filesOpenLocationAction = self._loadActionIcon("&Open Folder", "../resources/fa-free/solid/folder.svg")
        #self.filesOpenLocationAction.setStatusTip("Open Folder")
        #self.filesOpenLocationAction.triggered.connect(self.open_file_folder)

        # Task actions
        self.newTaskDirAction = self._loadActionIcon("&New", "../resources/fa-free/solid/folder-plus.svg")
        self.newTaskDirAction.setStatusTip("Creates the directory structure for a new scene")
        self.newTaskDirAction.triggered.connect(self.new_scene)

        self.publishTaskAction = self._loadActionIcon("&Publish", "../resources/fa-free/solid/share.svg")
        self.publishTaskAction.setStatusTip("Publish for review")
        self.publishTaskAction.triggered.connect(self.publish_scene)

        self.taskInfoAction = self._loadActionIcon("&Entity Info", "../resources/fa-free/solid/info-circle.svg")
        self.taskInfoAction.setStatusTip("View Entity Entity")
        self.taskInfoAction.triggered.connect(self.task_info) 

        self.openTaskFolderAction = self._loadActionIcon("&Open Folder", "../resources/fa-free/solid/folder.svg")
        self.openTaskFolderAction.setStatusTip("Open Task Folder")
        self.openTaskFolderAction.triggered.connect(self.open_task_folder)                  


    def _createContextMenu(self):
        # Setting contextMenuPolicy
        self.tableViewFiles.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableViewFiles.addAction(self.filesSelectAllAction)
        self.tableViewFiles.addAction(self.filesSelectNoneAction)
        #self.tableViewFiles.addAction(self.filesImportAction)
        #self.tableViewFiles.addAction(self.filesDownloadAction)
        # self.tableViewFiles.addAction(self.filesOpenLocationAction)


        # same for task table
        self.tableViewTasks.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.tableViewTasks.addAction(self.newTaskDirAction)
        self.tableViewTasks.addAction(self.publishTaskAction)
        self.tableViewTasks.addAction(self.taskInfoAction)
        self.tableViewTasks.addAction(self.openTaskFolderAction)
        #self.tableViewTasks.addAction(self.reviewTaskAction)
        #self.tableViewTasks.addAction(self.openEntitInfoAction)

    def open_file_folder(self):
        self.file_table_selection_changed()
        if self.selected_file:
            working_dir = self.swing_settings.swing_root()
            open_folder(resolve_content_path(self.selected_file["target_path"], working_dir))

    def open_task_folder(self):
        if self.selected_task:
            if "project_dir" in self.selected_task:
                working_dir = self.swing_settings.swing_root()
                if os.path.exists(working_dir) and os.path.isdir(working_dir):
                    open_folder(working_dir)        

    def version_check(self):
        version_check = VersionCheck(self)
        version_check.callback.loaded.connect(self.version_check_loaded)
        #version_check.run()
        self.threadpool.start(version_check)

    def version_check_loaded(self, version):
        print(version)
        if version:
            if SwingSettings._APP_VERSION == version:
                self.labelConnection.setText("Connected - v{}".format(version))
                self.labelConnection.mouseDoubleClickEvent = None
                #self.labelConnection.setHint("")
                #reply = QtWidgets.QMessageBox.question(self, 'Version', 'Thanks, you version is current !'.format(version), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            else:
                self.labelConnection.setText("New version available v{}".format(version))
                #self.labelConnection.setHint("Double click to update")
                self.labelConnection.setStyleSheet("color: green; font-weight: 600; ")
                self.labelConnection.mouseDoubleClickEvent = self.update_version
                ## self.update_version()

    def update_version(self, sender = None):
        reply = QtWidgets.QMessageBox.question(self, 'New Version found', 'Do you want to update ?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)        
        if reply == QtWidgets.QMessageBox.Yes:

            updater = SwingUpdater(self, os.getcwd())

            #updater.callback.loaded.connect(self.version_check_loaded)
            updater.run()
            #self.threadpool.start(updater)


    def set_handler(self, studio_handler):
        self.handler = studio_handler

        if self.handler.NAME == "StudioInterface":
            self.pushButtonClose.setText("Close")            
            self.pushButtonClose.clicked.connect(self.close_dialog)            
        else:
            self.pushButtonClose.setText("Hide")
            self.pushButtonClose.clicked.connect(self.hide_dialog)            

    def keyPressEvent(self, event):
        super(SwingGUI, self).keyPressEvent(event)

        event.accept()

    def selected_asset(self):
        return self.comboBoxAsset.currentData(QtCore.Qt.UserRole)

    def selected_shot(self):
        return self.comboBoxShot.currentData(QtCore.Qt.UserRole)

    def finished(self, code):
        write_log('we are finished %s\n' % str(code))            

    def open_file_item(self, index):
        item = self.treeWidgetFiles.itemFromIndex(index)

        if not item:
            return False

        file_name = item.data(index.row(), 0)
        file_list = self.get_file_selection_list()

        dialog = LoaderDialogGUI(self)
        dialog.load_files(file_list)
        dialog.set_file_name(file_name)
        dialog.show()        

    def set_loading(self, is_loading):
        self.loading = is_loading

    def set_to_shot(self):
        self.comboBoxShot.setEnabled(True)

        if self.radioButtonShot.isChecked() and (self.projectNav.get_sequence() is not None):
            self.load_shot_files(self.comboBoxShot.currentIndex())
            ## self.tasks_changed()

    def set_to_asset(self):
        self.comboBoxAsset.setEnabled(self.radioButtonAsset.isChecked())
        self.comboBoxAssetType.setEnabled(self.radioButtonAsset.isChecked())
        self.comboBoxShot.setEnabled(False)

        if self.radioButtonAsset.isChecked():
            if self.selected_asset():
                self.load_asset_files(self.comboBoxAsset.currentIndex())
                ## self.tasks_changed()
            else:
                if self.currentAssetType:
                    self.asset_type_changed(self.comboBoxAssetType.currentIndex())
                else:
                    if self.projectNav.get_project():
                        asset_loader = AssetTypeLoaderThread(self, self.projectNav.get_project())
                        asset_loader.callback.loaded.connect(self.asset_types_loaded)
                        self.threadpool.start(asset_loader)

    def get_current_selection(self):
        if self.radioButtonAsset.isChecked():
            return self.selected_asset()
        else:
            return self.selected_shot()

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

        selected = self.selected_shot()
        if selected:
            self.settings.setValue("last_shot", selected["name"])
        
        self.settings.endGroup()    

        self.settings.beginGroup("ProjectNav")
        self.settings.setValue("task_types", self.projectNav._user_task_types)
        self.settings.setValue("status_codes", self.projectNav._user_task_status)
        self.settings.endGroup()              

    # load main dialog state
    def readSettings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size", QtCore.QSize(400, 400)))
        #self.move(self.settings.value("pos", QtCore.QPoint(200, 200)))
        self.settings.endGroup()            

        self.settings.beginGroup("Selection")

        self.last_project = self.settings.value("last_project")
        self.last_sequences = self.settings.value("last_project")
        self.last_shot = self.settings.value("last_project")
        self.settings.endGroup()          

        self.project_root = self.swing_settings.swing_root()
        self.ffmpeg_bin = self.swing_settings.bin_ffmpeg()

    def open_connection_settings(self):
        dialog = SettingsDialog(self)

        if dialog.exec_():
            if not self.connected:
                write_log("loading settings")
                try:
                    if self.connect_to_server():
                        self.labelConnection.setText("Connected")
                        self.projectNav.load_open_projects()
                except:
                    write_log("error connecting to server, please check settings")
                #
            #

    def connect_to_server(self): 
        if self.connected and self.gazu_client:
            self.gazu_client = None
            self.connected = False

        password = self.swing_settings.swing_password()
        server = self.swing_settings.swing_server()
        email = self.swing_settings.swing_user()

        gazu.set_host("{}/api".format(server))
        try:
            self.gazu_client = gazu.log_in(email, password)
            self.connected = True
            self.user_email = email
            self.pushButtonConnect.setText("Connected")
        except:
            self.pushButtonConnect.setText("Reconnect")
            return False

        return True

    def hide_dialog(self):
        # hide ourselves in a DCC
        self.hide()

    def close_dialog(self):
        # otherwise exit
        self.close()

    def closeEvent(self, event):
        # in desktop, confirm and write 
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Exit', 'close {} ?'.format(SwingSettings._APP_NAME), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            # save settings
            self.writeSettings()      
            event.accept()
        else:
            event.ignore()        

    def selection_changed(self, source, selection): 
        ## write_log("[selection_changed]", source)
        if "project" in source and selection["is_loaded"]:
            ## self.projectNav.lock_ui(True)
            self.project_changed(self.projectNav.comboBoxProject.currentIndex())
        elif "episode_changed" in source:
            ## self.projectNav.lock_ui(True)
            self.episode_changed(self.projectNav.comboBoxEpisode.currentIndex())
        elif "sequence_changed" in source:
            self.sequence_changed(self.projectNav.comboBoxSequence.currentIndex())
            
        elif source in [ "task_types_changed", "status_codes_changed"]:
            ## self.projectNav.lock_ui(True)
            self.tasks_changed()

            if self.radioButtonAsset.isChecked():
                index = self.comboBoxAsset.currentIndex()
                if index >= 0:
                    self.load_asset_files(index)            
            else:
                index = self.comboBoxShot.currentIndex()
                if index >= 0:
                    self.load_shot_files(index)

    def project_changed(self, index):
        # reset file list and task list on project change
            
        self.tableViewFiles.setModel(None)
        self.tableViewTasks.setModel(None)

        self.currentProject = self.projectNav.get_project()
        if not self.currentProject:
            return False

        self.currentProjectIndex = index

        if self.currentProject:
            self.set_loading(True)     

            self.comboBoxAssetType.clear()
            self.comboBoxAsset.clear()
            self.comboBoxShot.clear()

            asset_loader = AssetTypeLoaderThread(self, self.currentProject)
            asset_loader.callback.loaded.connect(self.asset_types_loaded)
            self.threadpool.start(asset_loader)

            self.comboBoxAssetType.clear()
            if self.projectNav.get_sequence():
                self.sequence_changed(0)
            else:
                self.episode_changed(self.projectNav.comboBoxSequence.currentIndex())

            self.set_to_asset()
            self.tasks_changed()

    def tasks_changed(self):
        working_dir = self.swing_settings.swing_root()

        task_loader = TaskLoaderThread(self, self.projectNav, self.user_email, working_dir)
        task_loader.callback.loaded.connect(self.load_tasks)

        self.labelTaskTableSelection.setText("Loading tasks")
        self.progressBarTaskTable.setMaximum(0)
        self.tableViewTasks.setEnabled(False)
        self.toolButtonNew.setEnabled(False)
        self.toolButtonPublish.setEnabled(False)

        self.threadpool.start(task_loader)

    def episode_changed(self, index):
        #write_log("[episode_changed]")

        self.currentEpisode = self.projectNav.get_episode()
        if self.currentEpisode:
            self.currentEpisodeIndex = index

            if self.projectNav.comboBoxSequence.currentIndex() >= 0:
                self.load_shot_files(self.projectNav.comboBoxSequence.currentIndex())   

            elif self.comboBoxShot.currentIndex() >= 0:
                self.load_shot_files(self.comboBoxShot.currentIndex())

        self.tasks_changed()

        if self.projectNav.get_project():
            asset_loader = AssetTypeLoaderThread(self, self.projectNav.get_project())
            asset_loader.callback.loaded.connect(self.asset_types_loaded)
            self.threadpool.start(asset_loader)     

    def asset_types_loaded(self, data): 
        #write_log("[asset_types_loaded]")
        self.asset_types = data

        self.comboBoxAssetType.blockSignals(True)
        self.comboBoxAssetType.clear()
        for item in self.asset_types:
            #name = "{} {}".format(self.currentProject["code"], item["name"])            
            self.comboBoxAssetType.addItem(item["name"], userData = item)             
            # self.comboBoxAssetType.addItem(item["name"]) 
        self.comboBoxAssetType.blockSignals(False)                       
        self.comboBoxAssetType.setEnabled(True)

        if len(self.asset_types) > 0:
            self.asset_type_changed(0)

    def sequence_changed(self, index):
        #write_log("[sequence_changed]")
        
        self.comboBoxShot.blockSignals(True)                 
        self.comboBoxShot.clear()

        sequence = self.projectNav.get_sequence()
        if not sequence:
            return False

        episode = self.projectNav.get_episode()
        for item in sequence["shots"]:
            if episode:
                name = "{} / {} / {}".format(episode["name"], item["sequence_name"],  item["name"])
            else:
                name = "{} / {} / {}".format(item["sequence_name"],  item["name"])

            self.comboBoxShot.addItem(name, userData = item) 

        self.comboBoxShot.blockSignals(False)                 
        ## self.load_shot_files(0)

    def asset_type_changed(self, index):
        #write_log("[asset_type_changed]")
        self.currentAssetType = self.asset_types[index]

        project = self.projectNav.get_project()
        if project:
            loader = AssetLoaderThread(self, project, self.currentAssetType)
            loader.callback.loaded.connect(self.asset_loaded)
            self.threadpool.start(loader)

    def load_shot_files(self, index):
        if not self.projectNav.is_loaded():
            return 

        ## write_log("[selection_changed]", source)

        sequence = self.projectNav.get_sequence()
        if sequence:
            shots = sequence["shots"]
            if len(shots) > index:
                self.currentShot = shots[index]
                #write_log("load shot files {}".format(index))

                loader = EntityFileLoader(self, self.projectNav, self.currentShot, working_dir = self.swing_settings.swing_root())
                loader.callback.loaded.connect(self.load_files)

                self.labelFileTableSelection.setText("Loading files for {}".format(self.currentShot["name"]))
                self.progressBarFileTable.setMaximum(0)
                self.tableViewFiles.setEnabled(False)
                self.toolButtonFileTableSelectAll.setEnabled(False)
                self.toolButtonFileSelectNone.setEnabled(False)
                self.toolButtonImport.setEnabled(False)
                self.toolButtonDownload.setEnabled(False)

                self.threadpool.start(loader)
                ## loader.run()

    def asset_loaded(self, data): 
        #write_log("[asset_loaded]")

        self.comboBoxAsset.blockSignals(True)

        self.assets = data
        self.comboBoxAsset.clear()

        last = self.comboBoxAsset.currentIndex()

        asset_type = self.currentAssetType
        for item in self.assets:
            if asset_type:
                name = "{} / {}".format(asset_type["name"], item["name"]).strip()
            else:
                name = "{}".format(item["name"]).strip()
            self.comboBoxAsset.addItem(name, userData = item)     

        self.comboBoxAsset.blockSignals(False)            
        self.comboBoxAsset.setEnabled(True)       

    def load_asset_files(self, index):
        if not self.projectNav.is_loaded():
            return 

        asset = self.selected_asset()
        if not asset:
            return

        ## write_log("[selection_changed]", source)

        #write_log("load asset files {}".format(index))
        loader = EntityFileLoader(self, self.projectNav, asset, working_dir = self.swing_settings.swing_root())
        loader.callback.loaded.connect(self.load_files)

        self.labelFileTableSelection.setText("Loading files for {}".format(asset["name"]))
        self.progressBarFileTable.setMaximum(0)
        self.tableViewFiles.setEnabled(False)
        self.toolButtonFileTableSelectAll.setEnabled(False)
        self.toolButtonFileSelectNone.setEnabled(False)
        self.toolButtonImport.setEnabled(False)
        self.toolButtonDownload.setEnabled(False)

        self.threadpool.start(loader)       
        ## loader.run()

    def load_files(self, data):
        if len(data) == 0:
            self.tableViewFiles.setEnabled(False)
            self.files = []
            self.labelFileTableSelection.setText("")
            self.progressBarFileTable.setMaximum(1)            
            return 

        self.files = data[0]
        self.entity = data[1]

        self.tableModelFiles = FileTableModel(self, working_dir = self.swing_settings.swing_root(), items = self.files)
        setup_file_table(self.tableModelFiles, self.tableViewFiles)        

        selectionModel = self.tableViewFiles.selectionModel()
        selectionModel.selectionChanged.connect(self.file_table_selection_changed)   

        self.labelFileTableSelection.setText("")
        self.progressBarFileTable.setMaximum(1)

        if len(self.files) > 0:
            self.labelFileTableSelection.setText("Files: {}".format(self.entity["name"]))

            self.tableViewFiles.setEnabled(True)
            self.toolButtonFileTableSelectAll.setEnabled(True)
            self.toolButtonFileSelectNone.setEnabled(True)
            self.toolButtonImport.setEnabled(True)
            self.toolButtonDownload.setEnabled(True)          
        else:
            self.labelFileTableSelection.setText("No files found: {}".format(self.entity["name"]))


    def select_row(self, index):
        self.tableViewFiles.model().setData(index, QtCore.Qt.Checked, QtCore.Qt.EditRole)
        self.tableViewFiles.model().layoutChanged.emit()
        # self.tableViewFiles.update()
        # print("current row is %d", index.row())

    def file_table_double_click(self, index):
        #row_index = index.row()
        self.selected_file = self.tableViewFiles.model().data(index, QtCore.Qt.UserRole)
        if self.selected_file:
            working_dir = self.swing_settings.swing_root()
            set_target(self.selected_file, working_dir)

            if os.path.isfile(self.selected_file["target_path"]):
                reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(os.path.dirname(self.selected_file["target_path"]))
                    #open_folder(os.path.dirname(self.selected_file["target_path"]))
                    return True

            dialog = LoaderDialogGUI(self, self.handler, self.get_current_selection())
            dialog.load_files(self.files)
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
                self.toolButtonLoad.setEnabled(self.selected_file is not None)
                self.toolButtonImport.setEnabled(self.selected_file is not None)

            except:
                pass

        return True

    def load_tasks(self, data):
        self.tasks = data["tasks"]

        tableModel = TaskTableModel(self, self.tasks)

        # create the sorter model
        sorterModel = QtCore.QSortFilterProxyModel()
        sorterModel.setSourceModel(tableModel)
        sorterModel.setFilterKeyColumn(TaskTableModel.COL_ENTITY)

        self.tableViewTasks.setModel(sorterModel)
        self.tableViewTasks.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableViewTasks.setSortingEnabled(True)
        self.tableViewTasks.sortByColumn(TaskTableModel.COL_ENTITY, QtCore.Qt.AscendingOrder)

        selectionModel = self.tableViewTasks.selectionModel()
        selectionModel.selectionChanged.connect(self.task_table_selection_changed)         

        self.tableViewTasks.verticalHeader().setDefaultSectionSize(self.tableViewTasks.verticalHeader().minimumSectionSize())   

        hh = self.tableViewTasks.horizontalHeader()
        hh.setMinimumSectionSize(100)
        hh.setDefaultSectionSize(hh.minimumSectionSize())
        hh.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)        

        self.progressBarTaskTable.setMaximum(1)
        if len(self.tasks) > 0:
            self.labelTaskTableSelection.setText("Tasks: {} {}".format(data["project"]["name"], data["episode"]["name"]))
            self.tableViewTasks.setEnabled(True)
            self.toolButtonNew.setEnabled(True)
            self.toolButtonPublish.setEnabled(True)        
        else:
            self.labelTaskTableSelection.setText("No tasks found for {} {}".format(data["project"]["name"], data["episode"]["name"]))

    def task_table_selection_changed(self):
        if not (self.tableViewTasks.selectedIndexes()):
            return False

        idx = self.tableViewTasks.selectedIndexes()
        for index in idx:
            try:
                self.selected_task = self.tableViewTasks.model().data(index, QtCore.Qt.UserRole)

                self.toolButtonNew.setEnabled(self.selected_task is not None)
                self.toolButtonPublish.setEnabled(self.selected_task is not None)
                self.pushButtonPlayblast.setEnabled(self.selected_task is not None)
                break
            except:
                pass

        return True   

    def task_table_double_click(self, index):
        self.selected_task = self.tableViewTasks.model().data(index, QtCore.Qt.UserRole)
        if self.selected_task:
            if "project_dir" in self.selected_task:
                project_dir = self.selected_task["project_dir"]
                if os.path.exists(project_dir) and os.path.isdir(project_dir):
                    count = fcount(project_dir)
                    if count > 0:
                        self.publish_scene()
                    else:
                        open_folder(project_dir)
                else:
                    dialog = CreateDialogGUI(self, self.handler, self.selected_task)
                    dialog.resize(self.size())
                    dialog.setWorkingDir(project_dir)
                    dialog.show()                     


    def breakout_dialog(self):
        if self.projectNav.get_project() and self.projectNav.get_episode():
            dialog = BreakoutUploadDialog(self)
            dialog.set_project(self.projectNav.get_project())
            dialog.set_episode(self.projectNav.get_episode())
            dialog.set_sequence_index(self.projectNav.comboBoxSequence.currentIndex())
            dialog.exec_()
        else:
            QtWidgets.QMessageBox.information(self, 'Break Out', 'Please select a project and an episode first')  

    def playlist_dialog(self):
        if self.projectNav.get_project() and self.projectNav.get_episode():
            dialog = PlaylistDialog(self)
            dialog.set_project(self.projectNav.get_project())

            dialog.set_selection(self.projectNav.get_project(), self.projectNav.get_episode())
            dialog.exec_()
        else:
            QtWidgets.QMessageBox.information(self, 'Playlists', 'Please select a project')  


    def search_files_dialog(self):
        dialog = SearchFilesDialog(self.projectNav, self.handler, self.get_current_selection())
        dialog.exec_()


    def playblast_dialog(self):
        dialog = SwingPlayblastUi()
        dialog.show()
        
        # self.handler.on_playblast()

    def dcc_tools_dialog(self):
        dialog = DCCToolsDialog(self, self.handler, self.get_current_selection())
        #dialog.resize(self.size())
        dialog.exec_()

    def download_files(self):
        files = []
        for row in range(self.tableViewFiles.model().rowCount()):
            index = self.tableViewFiles.model().index(row, 0)
            if self.tableViewFiles.model().data(index, QtCore.Qt.DisplayRole):
                item = self.tableViewFiles.model().data(index, QtCore.Qt.UserRole)
                files.append(item)

        if len(files) == 0:
            dialog = DownloadDialogGUI(self, self.handler, self.projectNav, self.get_current_selection())
        else:
            dialog = DownloadDialogGUI(self, self.handler, self.projectNav, self.get_current_selection(), files)

        dialog.resize(self.size())
        dialog.show()

    def load_asset(self):
        dialog = LoaderDialogGUI(self, self.handler, self.get_current_selection())
        dialog.load_files(self.tableModelFiles.items)        

        if self.selected_file:
            dialog.set_selected(self.selected_file)

        dialog.show()

    def load_shot_info(self):
        self.set_to_shot()
        if self.selected_shot():
            dialog = EntityInfoDialog(self, self.projectNav, self.selected_shot(),  self.handler)
            dialog.resize(self.size())
            dialog.show()

    def load_asset_info(self):
        self.set_to_asset()
        if self.selected_asset():
            dialog = EntityInfoDialog(self, self.projectNav, self.selected_asset(), self.handler)
            dialog.resize(self.size())
            dialog.show()

    def publish_scene(self):
        if self.selected_task:        
            dialog = PublishDialogGUI(self, self.projectNav, self.handler, self.selected_task)
            if "project_dir" in self.selected_task:
                project_dir = self.selected_task["project_dir"]
                dialog = PublishDialogGUI(self, self.projectNav, self.handler, self.selected_task)

                if os.path.exists(project_dir) and os.path.isdir(project_dir):
                    dialog.set_working_dir(project_dir)

                dialog.show()

    def new_scene(self):
        if self.selected_task:
            dialog = CreateDialogGUI(self, self.handler, self.selected_task)
            dialog.resize(self.size())
            dialog.show() 

    def task_info(self):
        if self.selected_task:
            entity_id = self.selected_task["entity_id"]
            dialog = EntityInfoDialog(self, self.projectNav, entity_id, self.handler)
            dialog.resize(self.size())
            dialog.show()

'''
    CreateDialog class
    ################################################################################
'''

class CreateDialogGUI(QtWidgets.QDialog, Ui_CreateDialog):

    def __init__(self, parent = None, handler = None, task = None):
        super(CreateDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler
        self.handler.on_create = self.on_create

        self.shot = None
        self.asset = None
        self.url = None
        self.task = task
        self.set_ui_enabled(False)

        self.threadpool = QtCore.QThreadPool.globalInstance()

        loader = EntityLoaderThread(self, self.task["entity_id"])
        loader.callback.loaded.connect(self.entity_loaded)
        self.threadpool.start(loader)

        loader = TaskFileInfoThread(self, self.task, self.swing_settings.swing_root())
        loader.callback.loaded.connect(self.task_loaded)
        self.threadpool.start(loader)

        loader = SoftwareLoader(self)            
        loader.callback.loaded.connect(self.software_loaded)
        self.threadpool.start(loader)

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonImport.clicked.connect(self.process)

        self.setWorkingDir(task["project_dir"])
        

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')        

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
                if self.task["task_type"]["short_name"]:
                    sections.append(self.task["task_type"]["short_name"])          
                else:
                    sections.append(self.task["task_type"]["name"])          
                self.task_type_name = self.task["task_type"]["name"]

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
                if self.asset_type_name in StudioInterface.ASSET_TYPE_LOOKUP:
                    sections.append(StudioInterface.ASSET_TYPE_LOOKUP[self.asset_type_name])                     
                else:
                    sections.append(self.asset_type_name)                 

            self.asset_name = self.entity["name"].strip() 
            sections.append(self.asset_name)

            if "task_type" in self.task:
                if self.task["task_type"]["short_name"]:
                    sections.append(self.task["task_type"]["short_name"])          
                else:
                    sections.append(self.task["task_type"]["name"])          
                self.task_type_name = self.task["task_type"]["name"]

            self.lineEditEntity.setText(friendly_string("_".join(sections).lower()))

            self.textEditShotInfo.setText(self.asset["description"].strip())
            self.lineEditFrameIn.setText("")
            self.lineEditFrameIn.setEnabled(False)
            self.lineEditFrameOut.setText("")
            self.lineEditFrameOut.setEnabled(False)
            self.lineEditFrameCount.setText("")
            self.lineEditFrameCount.setEnabled(False)         

        self.toolButtonWeb.setEnabled(self.url is not None)
        self.set_ui_enabled(True)
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
        self.lineEditFrameCount.setEnabled(status)
        self.lineEditWorkingDir.setEnabled(status)
        self.toolButtonWorkingDir.setEnabled(status)
        self.comboBoxSoftware.setEnabled(status)

        self.pushButtonImport.setEnabled(status)
        self.pushButtonCancel.setEnabled(status)

    def process(self):
        self.append_status("Creating new scene")

        mode = "working"
        software = self.software[self.comboBoxSoftware.currentIndex()]
        name = "{}{}".format(self.lineEditEntity.text().strip(), software["file_extension"])
        workingDir = self.lineEditWorkingDir.text().strip()

        # only create working files on uploads
        # working_file = gazu.files.new_working_file(self.task, name = name, mode = mode, software = software)

        # call handler
        try:
            self.append_status("Create new project: {} {} {}".format(name, workingDir, software['name']))

            if (self.handler.on_create(source = name, working_dir = workingDir, software = software)):
                QtWidgets.QMessageBox.information(self, 'Swing: Create', 'Created folder {}'.format(workingDir), QtWidgets.QMessageBox.Ok)                        
            else:
                self.append_status("Error creating new scene")

            if self.type == "Shot":
                self.handler.set_globals(project = self.project_name, episode = self.episode_name, sequence = self.sequence_name, task = self.task_type_name, shot = self.shot_name, frame_in = self.lineEditFrameIn.text(), frame_out = self.lineEditFrameOut.text(), frame_count = self.lineEditFrameCount.text())
            else:
                self.handler.set_globals(project = self.project_name, asset_type = self.asset_type_name, task = self.task_type_name, asset = self.asset_name)

            self.append_status("Set globals")
        except:
            traceback.print_exc(file=sys.stdout)          

        self.close()
    # process

    def on_create(self, **kwargs):
        source = kwargs["source"]
        directory = kwargs["working_dir"]
        software = kwargs["software"]

        try:
            os.makedirs(directory, exist_ok = True)
            os.startfile(directory)
            print("Created working directory for {} {}".format(source, directory))
        except:
            print("Error creating directory for {} {}".format(source, directory))
            return False

        return True
