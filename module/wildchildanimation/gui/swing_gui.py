# -*- coding: utf-8 -*-
# PyQt Gui plugin for Treehouse
#
# version: 1.000
# date: 18 Feb 2021
#
#############################
import os
import sys
import traceback

# Qt High DPI 
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1

import gazu

from wildchildanimation.gui.background_workers import AssetLoaderThread, AssetTypeLoaderThread, EntityFileLoader, SwingUpdater, TaskLoaderThread, VersionCheck

from wildchildanimation.gui.downloads import DownloadDialogGUI
from wildchildanimation.gui.playlists import PlaylistDialog
from wildchildanimation.gui.breakout import BreakoutUploadDialog

from wildchildanimation.gui.swing_tables import FileTableModel, TaskTableModel, setup_file_table
from wildchildanimation.gui.swing_utils import load_combo, fcount, open_folder, resolve_content_path, resource_path, set_button_icon, set_target, write_log

from wildchildanimation.gui.swing_desktop import Ui_SwingMain
from wildchildanimation.gui.project_nav import ProjectNavWidget

from wildchildanimation.studio.studio_interface import StudioInterface

from wildchildanimation.gui.settings import SwingSettings, SettingsDialog
from wildchildanimation.gui.upload_monitor import UploadMonitorDialog

'''
    SwingGUI Main class
    ################################################################################
'''
class SwingGUI(QtWidgets.QDialog, Ui_SwingMain):
    swing_settings = None

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

    file_monitor = None

    @classmethod
    def get_instance(cls, handler = StudioInterface()):
        if not cls.dlg_instance:
            cls.dlg_instance = SwingGUI(studio_handler = handler)
        return cls.dlg_instance
    dlg_instance = None        

    @classmethod
    def show_dialog(cls, handler = StudioInterface()):
        if SwingGUI.get_instance(handler).isHidden():
            SwingGUI.get_instance(handler).show()
        else:
            SwingGUI.get_instance(handler).raise_()
            SwingGUI.get_instance(handler).activateWindow()    

    def build_shelf(self):
        self.handler.build_shelf(self)

    def keyPressEvent(self, event):
        super(SwingGUI, self).keyPressEvent(event)            

    def __init__(self, parent = None, studio_handler = None):
        super(SwingGUI, self).__init__(parent) # Call the inherited classes __init__ method
        
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint ^ QtCore.Qt.WindowMinMaxButtonsHint)

        # setup to hide in a dcc
        self.set_enabled(False)
        self.set_handler(studio_handler)

        self.connect(self, QtCore.SIGNAL("finished(int)"), self.finished)
        self.setWindowTitle("{} v{}".format(SwingSettings._APP_NAME, SwingSettings._APP_VERSION))

        resource_file = resource_path("../resources/swing_logo_white_small.png")
        if os.path.exists(resource_file):
            icon = QtGui.QIcon(resource_file)
            self.setWindowIcon(icon)

        self.swing_settings = SwingSettings.get_instance()

        self.nav = ProjectNavWidget()
        self.nav.signal.selection_changed.connect(self.selection_changed)        

        self.horizontalLayoutProject.addWidget(self.nav)
        
        self.comboBoxAsset.currentIndexChanged.connect(self.load_asset_files)
        self.comboBoxShot.currentIndexChanged.connect(self.load_shot_files)    

        self.toolButtonSettings.clicked.connect(self.open_connection_settings)
        self.toolButtonConnect.clicked.connect(self.connect_to_server)

        self.toolButtonImport.clicked.connect(self.load_asset)

        self.toolButtonDownload.clicked.connect(self.download_files)
        self.toolButtonPublish.clicked.connect(self.on_publish)

        self.toolButtonPlayblast.clicked.connect(self.on_playblast)
        self.toolButtonExport.clicked.connect(self.on_export)
        self.toolButtonNew.clicked.connect(self.on_create)
        
        self.toolButtonLayout.clicked.connect(self.breakout_dialog)
        self.toolButtonLayout.setEnabled(False)

        self.toolButtonPlaylists.clicked.connect(self.on_playlists)
        self.toolButtonPlaylists.setEnabled(False)

        self.toolButtonSearchFiles.clicked.connect(self.on_search)

        self.nav.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.nav.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.nav.comboBoxSequence.currentIndexChanged.connect(self.sequence_changed)

        self.comboBoxAssetType.currentIndexChanged.connect(self.asset_type_changed)      

        self.radioButtonShot.toggled.connect(self.set_to_shot)
        self.radioButtonAsset.toggled.connect(self.set_to_asset)

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
        set_button_icon(self.toolButtonFileTableSelectAll, "../resources/fa-free/solid/plus.svg")

        self.toolButtonFileSelectNone.clicked.connect(self.select_no_files)
        set_button_icon(self.toolButtonFileSelectNone, "../resources/fa-free/solid/minus.svg")

        self.toolButtonUploads.clicked.connect(self.show_upload_monitor)

        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.read_settings()
        self._createActions()
        self._createContextMenu()

        self.threadpool = QtCore.QThreadPool.globalInstance()

        if self.connect_to_server():
            self.labelConnection.setText("Connected")
            self.nav.load_open_projects()
            self.version_check()
            self.set_enabled(True)

        ## Don't do playlists yet
        ##self.toolButtonPlaylists.setVisible(False)

    def get_file_monitor(self):
        if self.file_monitor == None:
            self.file_monitor = UploadMonitorDialog(self)
        return self.file_monitor

    def show_upload_monitor(self):
        self.get_file_monitor().show()

    def set_enabled(self, enabled):
        self.toolButtonPlayblast.setEnabled(enabled)
        self.toolButtonLoad.setEnabled(enabled)
        self.toolButtonExport.setEnabled(enabled)
        self.toolButtonLayout.setEnabled(enabled)
        self.toolButtonSearchFiles.setEnabled(enabled)
        self.radioButtonAsset.setEnabled(enabled)
        self.radioButtonShot.setEnabled(enabled)
        self.tabWidget.setEnabled(enabled)
        self.toolButtonAssetInfo.setEnabled(enabled)
        self.toolButtonShotInfo.setEnabled(enabled)

        self.toolButtonNew.setEnabled(enabled)
        self.toolButtonPublish.setEnabled(enabled)
        self.toolButtonFileTableSelectAll.setEnabled(enabled)
        self.toolButtonFileSelectNone.setEnabled(enabled)
        self.toolButtonImport.setEnabled(enabled)
        self.toolButtonDownload.setEnabled(enabled)

        self.comboBoxAsset.setEnabled(enabled)
        self.comboBoxAssetType.setEnabled(enabled)
        self.comboBoxShot.setEnabled(enabled)

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

        # Task actions
        self.newTaskDirAction = self._loadActionIcon("&New", "../resources/fa-free/solid/folder-plus.svg")
        self.newTaskDirAction.setStatusTip("Creates the directory structure for a new scene")
        self.newTaskDirAction.triggered.connect(self.on_create)

        self.publishTaskAction = self._loadActionIcon("&Publish", "../resources/fa-free/solid/share.svg")
        self.publishTaskAction.setStatusTip("Publish for review")
        self.publishTaskAction.triggered.connect(self.on_publish)

        self.taskInfoAction = self._loadActionIcon("&Entity Info", "../resources/fa-free/solid/info-circle.svg")
        self.taskInfoAction.setStatusTip("View Entity Entity")
        self.taskInfoAction.triggered.connect(self.task_info) 

        self.openTaskFolderAction = self._loadActionIcon("&Open Folder", "../resources/fa-free/solid/folder.svg")
        self.openTaskFolderAction.setStatusTip("Open Task Folder")
        self.openTaskFolderAction.triggered.connect(self.open_task_folder)                          

        self.createTaskFolderAction = self._loadActionIcon("&Create Folders", "../resources/fa-free/solid/folder-plus.svg")
        self.createTaskFolderAction.setStatusTip("Create task folders for all selected tasks")
        self.createTaskFolderAction.triggered.connect(self.create_task_folder)   


    def _createContextMenu(self):
        self.tableViewFiles.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableViewFiles.addAction(self.filesSelectAllAction)
        self.tableViewFiles.addAction(self.filesSelectNoneAction)

        # same for task table
        self.tableViewTasks.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.tableViewTasks.addAction(self.newTaskDirAction)
        self.tableViewTasks.addAction(self.publishTaskAction)
        self.tableViewTasks.addAction(self.taskInfoAction)
        self.tableViewTasks.addAction(self.openTaskFolderAction)
        self.tableViewTasks.addAction(self.createTaskFolderAction)

    def open_file_folder(self):
        self.file_table_selection_changed()
        if self.selected_file:
            working_dir = self.swing_settings.swing_root()
            open_folder(resolve_content_path(self.selected_file["target_path"], working_dir))

    def open_task_folder(self):
        if self.selected_task:
            if "project_dir" in self.selected_task:
                working_dir = self.selected_task["project_dir"]
            else:
                working_dir = self.swing_settings.swing_root()

            if os.path.exists(working_dir) and os.path.isdir(working_dir):
                open_folder(working_dir)        

    def create_task_folder(self):
        created = 0
        for item in self.tableViewTasks.selectionModel().selectedRows():
            row = item.row()
            task = self.tableViewTasks.model().data(self.tableViewTasks.model().index(row, 0), role = QtCore.Qt.UserRole)
            if "project_dir" in task:
                working_dir = task["project_dir"]
                if not os.path.exists(working_dir):
                    try:
                        os.makedirs(working_dir, exist_ok = True)
                        created += 1
                    except:
                        print("Error creating folder: {}".format(working_dir))
        if created > 0:
            QtWidgets.QMessageBox.question(self, 'Swing: Tasks', 'Created {} new working folders'.format(created), QtWidgets.QMessageBox.Ok)                    


    def version_check(self):
        version_check = VersionCheck(self)
        version_check.callback.loaded.connect(self.version_check_loaded)
        self.threadpool.start(version_check)

    def version_check_loaded(self, version):
        if version:
            if SwingSettings._APP_VERSION == version:
                self.labelConnection.setText("Connected - v{}".format(version))
                self.labelConnection.mouseDoubleClickEvent = None
            else:
                self.labelConnection.setText("New version available v{}".format(version))
                self.labelConnection.setStyleSheet("color: green; font-weight: 600; ")
                self.labelConnection.mouseDoubleClickEvent = self.update_version
                ## self.update_version()
            print("{} {}".format(SwingSettings._APP_NAME, version))

    def update_version(self, sender = None):
        reply = QtWidgets.QMessageBox.question(self, 'New Version found', 'Do you want to update ?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)        
        if reply == QtWidgets.QMessageBox.Yes:

            updater = SwingUpdater(self, os.getcwd())
            self.threadpool.start(updater)

    def set_handler(self, studio_handler):
        self.handler = studio_handler

        if not self.handler.NAME == "MayaStudioHandler":
            self.toolButtonPlayblast.setVisible(False)
            self.toolButtonExport.setVisible(False)

            self.toolButtonClose.setText(" Close")            
            self.toolButtonClose.clicked.connect(self.close_dialog)            
        else:
            self.toolButtonClose.setText(" Hide")
            self.toolButtonClose.clicked.connect(self.hide_dialog)            

    def keyPressEvent(self, event):
        super(SwingGUI, self).keyPressEvent(event)

        event.accept()

    def selected_asset(self):
        return self.comboBoxAsset.currentData(QtCore.Qt.UserRole)

    def selected_shot(self):
        return self.comboBoxShot.currentData(QtCore.Qt.UserRole)

    def finished(self, code):
        write_log('we are finished %s\n' % str(code))            

    def set_to_shot(self):
        self.comboBoxShot.setEnabled(True)

        if self.radioButtonShot.isChecked() and (self.nav.get_sequence() is not None):

            self.load_shot_files(self.comboBoxShot.currentIndex())
            ## self.tasks_changed()
        self.tasks_changed()

    def set_to_asset(self):
        self.comboBoxAsset.setEnabled(self.radioButtonAsset.isChecked())
        self.comboBoxAssetType.setEnabled(self.radioButtonAsset.isChecked())
        self.comboBoxShot.setEnabled(False)

        if self.radioButtonAsset.isChecked():
            if self.selected_asset():
                self.load_asset_files(self.comboBoxAsset.currentIndex())
            else:
                if self.currentAssetType:
                    self.asset_type_changed(self.comboBoxAssetType.currentIndex())
                else:
                    if self.nav.get_project():
                        asset_loader = AssetTypeLoaderThread(self, self.nav.get_project()["project_id"])
                        asset_loader.callback.loaded.connect(self.asset_types_loaded)
                        self.threadpool.start(asset_loader)
        self.tasks_changed()

    def get_current_selection(self):
        if self.radioButtonAsset.isChecked():
            return self.selected_asset()
        else:
            return self.selected_shot()

    def tab_changed(self, index):
        if self.radioButtonAsset.isChecked():
            return self.set_to_asset()
        else:
            return self.set_to_shot()        

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        if self.currentProject:
            self.settings.setValue("last_project", self.currentProject["project_id"])

        if self.currentSequencesIndex and len(self.currentSequences) > 0 and self.currentSequences[self.currentSequencesIndex]:
            self.settings.setValue("last_sequences", self.currentSequences[self.currentSequencesIndex]["id"])

        selected = self.selected_shot()
        if selected:
            self.settings.setValue("last_shot", selected["shot"])

        self.settings.endGroup()  

        self.settings.beginGroup(ProjectNavWidget.__class__.__name__)
        self.settings.setValue("task_types", self.nav._user_task_types)
        self.settings.setValue("status_codes", self.nav._user_task_status)
        self.settings.endGroup()              

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.resize(self.settings.value("size", QtCore.QSize(400, 400)))
        #self.move(self.settings.value("pos", QtCore.QPoint(200, 200)))

        self.last_project = self.settings.value("last_project")
        self.last_sequences = self.settings.value("last_project")
        self.last_shot = self.settings.value("last_project")
        self.project_root = self.swing_settings.swing_root()
        self.ffmpeg_bin = self.swing_settings.bin_ffmpeg()
        self.settings.endGroup()              

    def open_connection_settings(self):
        self.settingsDialog = SettingsDialog(parent = self)

        if self.settingsDialog.show():
            if not self.connected:
                write_log("loading settings")
                try:
                    if self.connect_to_server():
                        self.labelConnection.setText("Connected")
                        self.nav.load_open_projects()
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
            self.toolButtonConnect.setText("Connected")
        except:
            self.toolButtonConnect.setText("Reconnect")
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
            self.write_settings()      
            event.accept()
        else:
            event.ignore()        

    def selection_changed(self, source, selection): 
        if "project" in source and selection["is_loaded"]:

            ## self.nav.lock_ui(True)
            self.project_changed(self.nav.comboBoxProject.currentIndex())

        elif "episode_changed" in source:

            ## self.nav.lock_ui(True)
            self.episode_changed(self.nav.comboBoxEpisode.currentIndex())

        elif "sequence_changed" in source:

            self.sequence_changed(self.nav.comboBoxSequence.currentIndex())
            
        elif source in [ "task_types_changed", "status_codes_changed"]:
            ## self.nav.lock_ui(True)
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
        try:
            # reset file list and task list on project change
                
            self.tableViewFiles.setModel(None)
            self.tableViewTasks.setModel(None)

            self.currentProject = self.nav.get_project()
            if not self.currentProject:
                return False

            self.currentProjectIndex = index

            if self.currentProject:
                self.comboBoxAssetType.clear()
                self.comboBoxAsset.clear()
                self.comboBoxShot.clear()

                asset_loader = AssetTypeLoaderThread(self, self.currentProject["project_id"])
                asset_loader.callback.loaded.connect(self.asset_types_loaded)
                self.threadpool.start(asset_loader)

                if self.nav.get_sequence():
                    self.sequence_changed(0)
                else:
                    self.episode_changed(self.nav.comboBoxSequence.currentIndex())

                self.set_to_asset()
        except:
            write_log("project_changed: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)                

    def tasks_changed(self):
        try:
            if self.nav.is_task_types_filtered():
                task_types = self.nav.get_task_types()
            else:
                task_types = None

            if self.nav.is_status_types_filtered():
                status_types = self.nav.get_task_status
            else:
                status_types = None

            self.currentProject = self.nav.get_project()
            if not self.currentProject:
                return False

            self.currentEpisode = self.nav.get_episode()
            if not self.currentEpisode:
                episode_id = "All"
            else:
                episode_id = self.currentEpisode["episode_id"]

            parent = self.get_current_selection()

            parent_id = None
            if parent:
                if episode_id == 'All':
                    parent_id = None
                elif "shot_id" in parent:
                    parent_id = parent["shot_id"]
                else:
                    parent_id = parent["id"]            
            ##print("Parent {}".format(parent_id))

            task_loader = TaskLoaderThread(self, project_id = self.currentProject["project_id"], episode_id = episode_id, parent_id = parent_id, task_types=task_types, status_types=status_types)
            #print("Project {} Ep {} Parent {} TT {} ST {} ".format(self.currentProject["project_id"], episode_id, parent_id, task_types, status_types))
            task_loader.callback.loaded.connect(self.load_tasks)

            self.labelTaskTableSelection.setText("Loading tasks")
            self.progressBarTaskTable.setMaximum(0)
            self.tableViewTasks.setEnabled(False)
            self.toolButtonNew.setEnabled(False)
            self.toolButtonPublish.setEnabled(False)
            
            ##task_loader.run()
            self.threadpool.start(task_loader)
        except:
            write_log("tasks_changed: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)                


    def episode_changed(self, index):
        try:
            self.currentEpisode = self.nav.get_episode()
            if self.currentEpisode:
                self.currentEpisodeIndex = index

                if self.nav.comboBoxSequence.currentIndex() >= 0:
                    self.load_shot_files(self.nav.comboBoxSequence.currentIndex())   

                elif self.comboBoxShot.currentIndex() >= 0:
                    self.load_shot_files(self.comboBoxShot.currentIndex())

            ## self.tasks_changed()

            if self.nav.get_project():
                asset_loader = AssetTypeLoaderThread(self, self.nav.get_project()["project_id"])
                asset_loader.callback.loaded.connect(self.asset_types_loaded)
                self.threadpool.start(asset_loader)     

            if self.currentEpisode:
                is_main_pack = self.currentEpisode["episode"] == "all"
                self.toolButtonLayout.setEnabled(not is_main_pack)
                self.toolButtonPlaylists.setEnabled(not is_main_pack)

            self.tasks_changed()
        except:
            write_log("episode_changed: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)                


    def asset_types_loaded(self, data): 
        self.asset_types = data
        self.comboBoxAssetType = load_combo(self.comboBoxAssetType, self.asset_types)

        if len(self.asset_types) > 0:
            self.asset_type_changed(0)

    def sequence_changed(self, index):
        try:
            sequence = self.nav.get_sequence()

            if not sequence:
                return False

            self.comboBoxShot.blockSignals(True)                 
            self.comboBoxShot.clear()

            episode = self.nav.get_episode()
            if "shots" in sequence:
                for item in sequence["shots"]:
                    if episode:
                        name = "{} / {} / {}".format(episode["episode"], item["sequence"],  item["shot"])
                    else:
                        name = "{} / {} / {}".format(item["sequence"],  item["shot"])

                    self.comboBoxShot.addItem(name, userData = item) 
                self.comboBoxShot.setEnabled(True)
            else:
                self.comboBoxShot.setEnabled(False)

            self.comboBoxShot.blockSignals(False)    
            self.tasks_changed()             
            ## self.load_shot_files(0)
        except:
            write_log("sequence_changed: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)                


    def asset_type_changed(self, index):
        #write_log("[asset_type_changed]")
        if index < 0:
            return

        self.currentAssetType = self.asset_types[index]

        project = self.nav.get_project()
        if project:
            loader = AssetLoaderThread(self, project["project_id"], self.currentAssetType)
            loader.callback.loaded.connect(self.asset_loaded)
            self.threadpool.start(loader)

    def load_shot_files(self, index):
        if not self.nav.is_loaded():
            return 

        ## write_log("[selection_changed]", source)

        sequence = self.nav.get_sequence()
        if sequence and "shots" in sequence:
            shots = sequence["shots"]
            if len(shots) > index:
                self.currentShot = shots[index]
                #write_log("load shot files {}".format(index))

                loader = EntityFileLoader(self, self.currentShot["shot_id"], working_dir = self.swing_settings.swing_root(), task_types = self.nav.get_task_types(), status_types = self.nav.get_task_status())
                loader.callback.loaded.connect(self.load_files)

                self.labelFileTableSelection.setText("Loading files for {}".format(self.currentShot["shot"]))
                self.progressBarFileTable.setMaximum(0)
                self.tableViewFiles.setEnabled(False)
                self.toolButtonFileTableSelectAll.setEnabled(False)
                self.toolButtonFileSelectNone.setEnabled(False)
                self.toolButtonImport.setEnabled(False)
                self.toolButtonDownload.setEnabled(False)

                self.threadpool.start(loader)
                ## loader.run()

        self.tasks_changed()

    def asset_loaded(self, data): 
        #write_log("[asset_loaded]")

        self.comboBoxAsset.blockSignals(True)

        self.assets = data
        self.comboBoxAsset.clear()

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
        if not self.nav.is_loaded():
            return 

        asset = self.selected_asset()
        if not asset:
            return

        ## write_log("[selection_changed]", source)

        #write_log("load asset files {}".format(index))
        loader = EntityFileLoader(self, asset["id"], working_dir = self.swing_settings.swing_root(), task_types = self.nav.get_task_types(), status_types = self.nav.get_task_status())
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

            self.on_load()

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
            self.labelTaskTableSelection.setText("Tasks: {} {}".format(self.currentProject["project"], data["episode"]["name"]))
            self.tableViewTasks.setEnabled(True)
            self.toolButtonNew.setEnabled(True)
            self.toolButtonPublish.setEnabled(True)        
        else:
            self.labelTaskTableSelection.setText("No tasks found for {} {}".format(self.currentProject["project"], data["episode"]["name"]))

    def task_table_selection_changed(self):
        if not (self.tableViewTasks.selectedIndexes()):
            return False

        idx = self.tableViewTasks.selectedIndexes()
        for index in idx:
            try:
                self.selected_task = self.tableViewTasks.model().data(index, QtCore.Qt.UserRole)

                self.toolButtonNew.setEnabled(self.selected_task is not None)
                self.toolButtonPublish.setEnabled(self.selected_task is not None)
                self.toolButtonPlayblast.setEnabled(self.selected_task is not None)
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
                        self.on_publish()
                    else:
                        open_folder(project_dir)
                else:
                    self.handler.on_create(parent = self, handler = self.handler, task = self.selected_task)


    def breakout_dialog(self):
        if self.nav.get_project() and self.nav.get_episode():
            dialog = BreakoutUploadDialog(self)
            dialog.set_project(self.nav.get_project())
            dialog.set_episode(self.nav.get_episode())
            dialog.set_sequence(self.nav.get_sequence())
            dialog.exec_()
        else:
            QtWidgets.QMessageBox.information(self, 'Break Out', 'Please select a project and an episode first')  

    def on_playlists(self):
        if self.nav.get_project() and self.nav.get_episode():
            self.playlist_dialog = PlaylistDialog(self)
            self.playlist_dialog.set_project_episode(self.nav.get_project()["project_id"], self.nav.get_episode()["episode_id"], self.nav.get_task_types())

            self.playlist_dialog.exec_()
        else:
            QtWidgets.QMessageBox.information(self, 'Playlists', 'Please select a project and an episode first')  

    def download_files(self):
        files = []
        for row in range(self.tableViewFiles.model().rowCount()):
            index = self.tableViewFiles.model().index(row, 0)
            if self.tableViewFiles.model().data(index, QtCore.Qt.DisplayRole):
                item = self.tableViewFiles.model().data(index, QtCore.Qt.UserRole)
                files.append(item)

        if len(files) == 0:
            QtWidgets.QMessageBox.information(self, 'Swing: Downloader', 'Please select a file')  
            # self.downloadDialog = DownloadDialogGUI(parent = self, handler = self.handler, entity = self.get_current_selection(), task_types=self.nav.get_task_types(), status_types=self.nav.get_status_types())
        else:
            self.downloadDialog = DownloadDialogGUI(parent = self, handler = self.handler, file_list=files)

        self.downloadDialog.show()

    def load_asset(self):

        self.on_load(files = self.tableModelFiles.items)

    def load_shot_info(self):

        self.handler.on_entity_info(parent = self, entity_id = self.selected_shot()["shot_id"], task_types = self.nav.get_task_types())

    def load_asset_info(self):

        self.handler.on_entity_info(parent = self, entity_id = self.selected_asset()["id"], task_types = self.nav.get_task_types())

    # Studio Handlers 
    def on_create(self):
        if self.selected_task:
            self.handler.on_create(parent = self, handler = self.handler, task = self.selected_task)
            #dialog = SwingCreateDialog(self, self.handler, self.selected_task)
            #dialog.show()         

    def on_search(self):
        if self.nav.is_task_types_filtered():
            task_types = self.nav.get_task_types()
        else:
            task_types = None

        if self.nav.is_status_types_filtered():
            status_types = self.nav.get_task_status
        else:
            status_types = None

        parent = self.get_current_selection()

        parent_id = None
        if parent:
            if "shot_id" in parent:
                parent_id = parent["shot_id"]
            else:
                parent_id = parent["id"]                

        self.handler.on_search(parent = self, entity = parent_id, project = self.nav.get_project()["project_id"], task_types = task_types, status_types = status_types)

    def on_load(self, files = None):
        if not files:
            files = self.files

        parent = self.get_current_selection()

        parent_id = None
        if parent:
            if "shot_id" in parent:
                parent_id = parent["shot_id"]
            else:
                parent_id = parent["id"]                 

        self.handler.on_load(parent = self, entity = parent_id, files = files, selected = self.selected_file)

    def on_export(self):
        if self.selected_task:
            task_id = self.selected_task["id"]
            self.handler.on_export(parent = self, task_id = task_id)

    def on_playblast(self):

        self.handler.on_playblast()

    def on_publish(self):
        task_types = self.nav.get_task_types()
        status_types = self.nav.get_task_status()

        if self.selected_task:        
            project_dir = self.selected_task["project_dir"]            
            self.handler.on_publish(parent = self, task = self.selected_task, project_dir = project_dir, task_types = task_types, status_types = status_types, monitor = self.get_file_monitor())
 
    def task_info(self):
        if self.selected_task:
            entity_id = self.selected_task["entity_id"]

            self.handler.on_entity_info(parent = self, entity_id = entity_id, task_types = self.nav.get_task_types())

