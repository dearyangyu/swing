# -*- coding: utf-8 -*-
# PyQt Gui plugin for Treehouse
#
# version: 1.000
# date: 18 Feb 2021
#
#############################
_APP_NAME = "treehouse: swing"
_APP_VERSION = "0.0.15"
 
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

import wildchildanimation.gui.background_workers as bg

from wildchildanimation.gui.swing_utils import *

from wildchildanimation.gui.main_form import Ui_WcaMayaDialog
from wildchildanimation.gui.connection_dialog import Ui_ConnectionDialog
from wildchildanimation.gui.publish_dialog import Ui_PublishDialog

from wildchildanimation.gui.create_dialog import Ui_CreateDialog

from wildchildanimation.gui.playblast_dialog import Ui_PlayblastDialog

from wildchildanimation.gui.loader import *
from wildchildanimation.gui.references import *
from wildchildanimation.gui.search import *
from wildchildanimation.gui.downloads import *
from wildchildanimation.gui.publish import *
from wildchildanimation.gui.playlists import *
from wildchildanimation.gui.breakout import *
from wildchildanimation.gui.entity_info import *
from wildchildanimation.gui.dcc_tools import *

from wildchildanimation.gui.swing_tables import FileTableModel, TaskTableModel, CastingTableModel, load_file_table_widget, human_size

from wildchildanimation.gui.swing_desktop import Ui_SwingMain
from wildchildanimation.gui.project_nav import ProjectNavWidget

from wildchildanimation.studio_interface import StudioInterface

from wildchildanimation.gui.zurbrigg_playblast import *


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

    dlg_instance = None

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
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        # setup to hide in a dcc
        self.set_handler(studio_handler)

        self.connect(self, QtCore.SIGNAL("finished(int)"), self.finished)
        self.setWindowTitle("{} v{}".format(_APP_NAME, _APP_VERSION))

        resource_file = resource_path("../resources/swing_logo_white_small.png")
        if os.path.exists(resource_file):
            icon = QtGui.QIcon(resource_file)
            self.setWindowIcon(icon)

        QtCore.QCoreApplication.setOrganizationName("Wild Child Animation")
        QtCore.QCoreApplication.setOrganizationDomain("wildchildanimation.com")
        QtCore.QCoreApplication.setApplicationName(_APP_NAME)

        self.projectNav = ProjectNavWidget()
        self.projectNav.signal.selection_changed.connect(self.selection_changed)        

        self.horizontalLayoutProject.addWidget(self.projectNav)
        
        self.comboBoxAsset.currentIndexChanged.connect(self.load_asset_files)
        self.comboBoxShot.currentIndexChanged.connect(self.load_shot_files)    

        self.pushButtonSettings.clicked.connect(self.open_connection_settings)
        self.pushButtonConnect.clicked.connect(self.connect_to_server)

        self.pushButtonImport.clicked.connect(self.load_asset)
        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonPublish.clicked.connect(self.publish_scene)

        self.pushButtonPlayblast.clicked.connect(self.playblast_dialog)
        self.pushButtonExport.clicked.connect(self.dcc_tools_dialog)

        self.pushButtonNew.clicked.connect(self.new_scene)
        
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

        self.tableViewTasks.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewTasks.doubleClicked.connect(self.task_table_double_click)        

        self.toolButtonShotInfo.clicked.connect(self.load_shot_info)
        self.toolButtonAssetInfo.clicked.connect(self.load_asset_info)

        self.readSettings()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        if self.connect_to_server():
            self.labelConnection.setText("Connected")
            self.projectNav.load_open_projects()

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
                    if self.projectNav.get_project():
                        asset_loader = bg.AssetTypeLoaderThread(self, self.projectNav.get_project())
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

        password = load_keyring('swing', 'password', 'Not A Password')

        server = load_settings('server', 'https://production.wildchildanimation.com')
        email = load_settings('user', 'user@example.com')

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
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Exit', 'close {} ?'.format(_APP_NAME), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            # save settings
            self.writeSettings()      
            event.accept()
        else:
            event.ignore()        

    def selection_changed(self, source, selection): 
        #write_log("[selection_changed]", source)

        if "project" in source and selection["is_loaded"]:
            self.project_changed(self.projectNav.comboBoxProject.currentIndex())
        #self.comboBoxProject.setEnabled(True)

        #if self.first_load:
        #    self.first_load = False
        #    self.project_changed(self.currentProjectIndex)   

    def project_changed(self, index):
        #write_log("[project_changed]")

        self.currentProject = self.projectNav.get_project()
        if not self.currentProject:
            return False

        self.currentProjectIndex = index

        if self.currentProject:
            self.set_loading(True)     

            self.comboBoxAssetType.clear()
            self.comboBoxAsset.clear()
            self.comboBoxShot.clear()

            asset_loader = bg.AssetTypeLoaderThread(self, self.currentProject)
            asset_loader.callback.loaded.connect(self.asset_types_loaded)
            self.threadpool.start(asset_loader)

            self.comboBoxAssetType.clear()

            task_loader = bg.TaskLoaderThread(self, self.currentProject, self.user_email)
            task_loader.callback.loaded.connect(self.tasks_loaded)
            self.threadpool.start(task_loader)

            if self.projectNav.get_sequence():
                self.sequence_changed(0)
            else:
                self.episode_changed(self.projectNav.comboBoxSequence.currentIndex())

            self.set_to_asset()
            

    def episode_changed(self, index):
        #write_log("[episode_changed]")

        self.currentEpisode = self.projectNav.get_episode()
        if self.currentEpisode:
            self.currentEpisodeIndex = index

            if self.projectNav.comboBoxSequence.currentIndex() >= 0:
                self.load_shot_files(self.projectNav.comboBoxSequence.currentIndex())   

            elif self.comboBoxShot.currentIndex() >= 0:
                self.load_shot_files(self.comboBoxShot.currentIndex())

    def asset_types_loaded(self, data): 
        #write_log("[asset_types_loaded]")
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
        #write_log("[tasks_loaded]")

        self.tasks = data
        self.load_tasks(self.tasks)

    def sequence_changed(self, index):
        #write_log("[sequence_changed]")
        
        self.comboBoxShot.blockSignals(True)                 
        self.comboBoxShot.clear()

        have_shots = False
        sequence = self.projectNav.get_sequence()
        if not sequence:
            return False

        for item in sequence["shots"]:
            name = "{} {}".format(item["sequence_name"],  item["name"])
            self.comboBoxShot.addItem(item["name"]) 
            have_shots  = True

        self.comboBoxShot.blockSignals(False)                 
        self.load_shot_files(0)

    def asset_type_changed(self, index):
        #write_log("[asset_type_changed]")
        self.currentAssetType = self.asset_types[index]

        project = self.projectNav.get_project()
        if project:
            loader = bg.AssetLoaderThread(self, project, self.currentAssetType)
            loader.callback.loaded.connect(self.asset_loaded)
            self.threadpool.start(loader)

    def load_shot_files(self, index):
        sequence = self.projectNav.get_sequence()
        if sequence:
            self.currentShot = sequence["shots"][index]
            #write_log("load shot files {}".format(index))

            loader = bg.EntityFileLoader(self, self.currentShot, working_dir = load_settings("projects_root", os.path.expanduser("~")))
            loader.callback.loaded.connect(self.files_loaded)
            #loader.exec()
            self.threadpool.start(loader)

    def files_loaded(self, data):
        output_files = data["output_files"]
        working_files = data["working_files"]

        self.load_files(output_files, working_files)        
        #write_log("Loaded {} output files, {} working files".format(len(output_files), len(working_files)))

    def asset_loaded(self, data): 
        #write_log("[asset_loaded]")

        self.assets = data
        self.comboBoxAsset.clear()

        last = self.comboBoxAsset.currentIndex()
        for p in self.assets:
            name = "{}".format(p["name"]).strip()
            self.comboBoxAsset.addItem(name)     
        self.comboBoxAsset.setEnabled(True)       

    def load_asset_files(self, index):
        self.currentAsset = self.assets[index]

        #write_log("load asset files {}".format(index))
        loader = bg.EntityFileLoader(self, self.currentAsset, working_dir = load_settings("projects_root", os.path.expanduser("~")))
        loader.callback.loaded.connect(self.files_loaded)
        self.threadpool.start(loader)       
        ## loader.run()


    def load_files(self, output_files = None, working_files = None):
        self.files = []

        if output_files:
            for item in output_files:
                self.files.append(item)

        if working_files:
            for item in working_files:
                self.files.append(item)

        self.tableModelFiles = FileTableModel(self, self.files)

        # create the sorter model
        sorterModel = QtCore.QSortFilterProxyModel()
        sorterModel.setSourceModel(self.tableModelFiles)
        sorterModel.setFilterKeyColumn(0)

        # filter proxy model
        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.tableModelFiles)
        filter_proxy_model.setFilterKeyColumn(2) # third column        

        self.tableViewFiles.setModel(sorterModel)                
        self.tableViewFiles.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableViewFiles.setSortingEnabled(True)
        self.tableViewFiles.sortByColumn(0, QtCore.Qt.DescendingOrder)

        self.tableViewFiles.setColumnWidth(0, 300)
        self.tableViewFiles.setColumnWidth(1, 150)
        self.tableViewFiles.setColumnWidth(2, 75)
        self.tableViewFiles.setColumnWidth(3, 150)
        self.tableViewFiles.setColumnWidth(4, 350)
        self.tableViewFiles.setColumnWidth(6, 200)

        selectionModel = self.tableViewFiles.selectionModel()
        selectionModel.selectionChanged.connect(self.file_table_selection_changed)     

        self.tableViewFiles.verticalHeader().setDefaultSectionSize(self.tableViewFiles.verticalHeader().minimumSectionSize())        

        self.pushButtonDownload.setEnabled(len(self.files) > 0)    
        self.pushButtonImport.setEnabled(len(self.files) > 0)

    def file_table_double_click(self, index):
        #row_index = index.row()
        self.selected_file = self.tableViewFiles.model().data(index, QtCore.Qt.UserRole)
        if self.selected_file:
            working_dir = load_settings("projects_root", os.path.expanduser("~"))
            set_target(self.selected_file, working_dir)

            if os.path.isfile(self.selected_file["target_path"]):
                reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(os.path.dirname(self.selected_file["target_path"]))
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
                self.pushButtonLoad.setEnabled(self.selected_file is not None)
                self.pushButtonImport.setEnabled(self.selected_file is not None)

            except:
                pass

        return True

    def load_tasks(self, tasks = None):
        self.tasks = tasks
        tableModel = TaskTableModel(self, tasks)

        # create the sorter model
        sorterModel = QtCore.QSortFilterProxyModel()
        sorterModel.setSourceModel(tableModel)
        sorterModel.setFilterKeyColumn(3)

        self.tableViewTasks.setModel(sorterModel)
        self.tableViewTasks.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableViewTasks.setSortingEnabled(True)
        self.tableViewTasks.sortByColumn(4, QtCore.Qt.AscendingOrder)

        #self.tableViewTasks.setColumnWidth(0, 250)
        #self.tableViewTasks.setColumnWidth(1, 200)
        #self.tableViewTasks.setColumnWidth(2, 200)
        #self.tableViewTasks.setColumnWidth(3, 350)
        #self.tableViewTasks.setColumnWidth(4, 120)
        #self.tableViewTasks.setColumnWidth(5, 160)
        #self.tableViewTasks.setColumnWidth(6, 600)

        selectionModel = self.tableViewTasks.selectionModel()
        selectionModel.selectionChanged.connect(self.task_table_selection_changed)         

        self.tableViewTasks.verticalHeader().setDefaultSectionSize(self.tableViewTasks.verticalHeader().minimumSectionSize())   

        hh = self.tableViewTasks.horizontalHeader()
        hh.setMinimumSectionSize(100)
        hh.setDefaultSectionSize(hh.minimumSectionSize())
        hh.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)        

        #self.tableViewTasks.verticalHeader().setDefaultSectionSize(self.tableViewTasks.verticalHeader().minimumSectionSize())

        #tableViewPowerDegree->verticalHeader()->setDefaultSectionSize(tableViewPowerDegree->verticalHeader()->minimumSectionSize()); 
        # self.pushButtonPublish.setEnabled(len(tasks) > 0)

    def task_table_selection_changed(self):
        if not (self.tableViewTasks.selectedIndexes()):
            return False

        idx = self.tableViewTasks.selectedIndexes()
        for index in idx:
            try:
                self.selected_task = self.tableViewTasks.model().data(index, QtCore.Qt.UserRole)

                self.pushButtonNew.setEnabled(self.selected_task is not None)
                self.pushButtonPublish.setEnabled(self.selected_task is not None)
                self.pushButtonPlayblast.setEnabled(self.selected_task is not None)
                break
            except:
                pass

        return True   

    def task_table_double_click(self, index):
        self.selected_task = self.tableViewTasks.model().data(index, QtCore.Qt.UserRole)
        if self.selected_task:
            if "task_url" in self.selected_task and self.selected_task["task_url"]:
                link = self.selected_task["task_url"]
                if not QtGui.QDesktopServices.openUrl(link):
                    QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')                    


    def breakout_dialog(self):
        if self.projectNav.get_project() and self.projectNav.get_episode():
            dialog = BreakoutUploadDialog(self)
            dialog.set_project(self.projectNav.get_project())
            dialog.set_episode(self.projectNav.get_episode())
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
        dialog = SearchFilesDialog(self, self.handler, self.get_current_selection(), self.task_types)
        dialog.set_project(self.projectNav.get_project())

        dialog.exec_()


    def playblast_dialog(self):
        zurbrigg_playblast_dialog = ZurbriggPlayblastUi()
        zurbrigg_playblast_dialog.show()
        # self.handler.on_playblast()

    def dcc_tools_dialog(self):
        dialog = DCCToolsDialog(self, self.handler, self.get_current_selection())
        #dialog.resize(self.size())
        dialog.exec_()

    def download_files(self):
        dialog = DownloadDialogGUI(self, self.get_current_selection(), self.projectNav.get_task_types())
        dialog.resize(self.size())
        dialog.exec_()

    def load_asset(self):
        dialog = LoaderDialogGUI(self, self.handler, self.get_current_selection())
        dialog.resize(self.size())    

        dialog.load_files(self.tableModelFiles.items)
        if self.selected_file:
            dialog.set_selected(self.selected_file)

        dialog.show()

    def load_shot_info(self):
        if self.currentShot:
            dialog = EntityInfoDialog(self, self.currentShot, self.projectNav.get_task_types(), self.handler)
            dialog.resize(self.size())
            dialog.exec_()

    def load_asset_info(self):
        if self.currentAsset:
            dialog = EntityInfoDialog(self, self.currentAsset, self.projectNav.get_task_types(), self.handler)
            dialog.resize(self.size())
            dialog.exec_()

    def publish_scene(self):
        if self.selected_task:        
            dialog = PublishDialogGUI(self, self.handler, self.selected_task)
            dialog.resize(self.size())
            dialog.show()

    def new_scene(self):
        if self.selected_task:
            dialog = CreateDialogGUI(self, self.handler, self.selected_task)
            dialog.resize(self.size())
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

        self.lineEditFfprobeBin.setText(load_settings("ffprobe_bin", ""))
        self.toolButtonFfprobeBin.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonFfprobeBin.clicked.connect(self.select_ffprobe_bin)    

    def select_projects_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if directory:
            self.lineEditProjectsFolder.setText(directory)

    def select_ffmpeg_bin(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select ffmpeg binary')
        if binary:
            self.lineEditFfmpegBin.setText(binary[0])            

    def select_ffprobe_bin(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select ffprobe binary')
        if binary:
            self.lineEditFfprobeBin.setText(binary[0])            

    def save_settings(self):
        self.buttonBox.accepted.disconnect()

        save_settings('server', self.lineEditServer.text())
        save_settings('user', self.lineEditEmail.text())
        save_settings("projects_root", self.lineEditProjectsFolder.text())                            
        save_settings("ffmpeg_bin", self.lineEditFfmpegBin.text())    
        save_settings("ffprobe_bin", self.lineEditFfprobeBin.text())    

        save_password('swing', 'password', self.lineEditPassword.text())

        self.buttonBox.accepted.connect(self.save_settings)
        return True

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

        # call handler
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

        self.close()
    # process

