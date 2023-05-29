# -*- coding: utf-8 -*-
#
# Author: P Niemandt
# Date: 2022-11-30
# Version: 1.0
#
# Allows for Project Shot Selection to pass to Sequence Creator

import sys
import os
import gazu

from wildchildanimation.gui.swing_utils import load_keyring
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.background_workers import ProjectLoaderThread
from wildchildanimation.gui.swing_utils import connect_to_server
from wildchildanimation.gui.swing_tables import CheckBoxDelegate

from wildchildanimation.studio.utils.rename_asset_dialog import Ui_RenameAssetWidget

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1

class FileTableModel(QtCore.QAbstractTableModel):

    columns = [
        "Selected", "Path", "Name"
    ]    

    def __init__(self, parent, file_list = None):
        super(FileTableModel, self).__init__(parent)
        self.file_list = file_list
        if self.file_list:
            for item in self.file_list:
                item["selected"] = True

    def flags(self, index):
        col = index.column()
        if col in [0]:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled| QtCore.Qt.ItemIsEditable            
            
        return QtCore.Qt.ItemIsEnabled

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns)        

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])        

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            item = self.file_list[index.row()]
            col = index.column()

            if 0 == col:
                return item["selected"]
            elif 1 == col:
                return item["path"]
            elif 2 == col:
                return item["name"]    

    def rowCount(self, index):
        if self.file_list:
            return len(self.file_list)       
        return 0

class DirectoryTableModel(QtCore.QAbstractTableModel):

    columns = [
        "Selected", "Path"
    ]    

    def __init__(self, parent, file_list = None):
        super(DirectoryTableModel, self).__init__(parent)
        self.file_list = []

        if file_list:
            for item in file_list:
                row = {
                    "path": item,
                    "selected": True
                }
                self.file_list.append(row)

    def flags(self, index):
        col = index.column()
        if col in [0]:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled| QtCore.Qt.ItemIsEditable            
            
        return QtCore.Qt.ItemIsEnabled

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns)        

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])        

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            item = self.file_list[index.row()]
            col = index.column()

            if 0 == col:
                return item["selected"]
            elif 1 == col:
                return item["path"]

    def rowCount(self, index):
        if self.file_list:
            return len(self.file_list)       
        return 0        

class RenameAssetDialog(QtWidgets.QDialog, Ui_RenameAssetWidget):

    def __init__(self, parent = None):
        super(RenameAssetDialog, self).__init__(parent) # Call the inherited classes __init__ method    
        self.setupUi(self)
        self.setWindowTitle("Swing UE Asset Rename")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.read_settings()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxAssetType.currentIndexChanged.connect(self.asset_type_changed)
        self.comboBoxAssetName.currentIndexChanged.connect(self.asset_name_changed)

        if connect_to_server(SwingSettings.get_instance().swing_user(), SwingSettings.get_instance().swing_password()):
            self.load_open_projects()

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonOk.clicked.connect(self.process)        

    def get_project(self):
        project = self.comboBoxProject.currentData()
        if "project_id" in project:
            project = gazu.project.get_project(project["project_id"])

        return project

    def get_asset_type(self):
        return self.comboBoxAssetType.currentData()

    def set_project(self, index):
        self.comboBoxProject.setCurrentIndex(index)
        self.project_changed(index)

    def get_asset(self):
        return self.comboBoxAssetName.currentData()

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()

        self.settings.beginGroup(self.__class__.__name__)
        self.settings.setValue("pos", self.pos())
        #self.settings.setValue("working_dir", self.lineEditRenderPath.text())

        #self.settings.setValue("handles_in", self.spinBoxHandlesIn.value())
        #self.settings.setValue("handles_out", self.spinBoxHandlesOut.value())

        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        #self.working_dir = self.settings.value("working_dir", "~")

    def load_open_projects(self):
        self.comboBoxProject.clear()

        loader = ProjectLoaderThread(self)
        loader.callback.loaded.connect(self.projects_loaded)
        
        self.threadpool.start(loader)  

    def projects_loaded(self, results): 
        project_dict = {}
        for item in results["projects"]:
            project_id = item["project_id"]
            if not project_id in project_dict:
                project_dict[project_id] = { "project_id": project_id, "project": item["project"], "episodes": [] }

            project = project_dict[project_id]
            project["episodes"].append(item)

        self._projects = project_dict.values()

        self.comboBoxProject.blockSignals(True)
        self.comboBoxProject.clear()

        for item in self._projects:
            self.comboBoxProject.addItem(item["project"], userData = item)
        self.comboBoxProject.blockSignals(False)

        self.comboBoxAssetType.clear()
        self.comboBoxAssetName.clear()

        self.project_changed(self.comboBoxProject.currentIndex())

    def project_changed(self, index):
        project = self.comboBoxProject.itemData(index)

        if "project_id" in project:
            project = gazu.project.get_project(project["project_id"])

        self.comboBoxAssetType.clear()
        self.comboBoxAssetName.clear()

        self.comboBoxAssetType.blockSignals(True)

        # Add Main Pack Episode placeholder for Asset Tasks
        self.asset_types = gazu.asset.all_asset_types_for_project(project)
        for item in self.asset_types:
            self.comboBoxAssetType.addItem(item["name"], userData = item)
            
        self.comboBoxAssetType.blockSignals(False)
        self.comboBoxAssetType.setCurrentIndex(0)   

        self.asset_type_changed(self.comboBoxAssetType.currentIndex())
        ## self.sequence_changed(self.comboBoxSequence.currentIndex())   
        #        

    def asset_type_changed(self, index):
        project = self.get_project()

        if index < 0:
            return False
        
        asset_type = self.get_asset_type()

        self.assets = gazu.asset.all_assets_for_project_and_type(project, asset_type)

        self.comboBoxAssetName.blockSignals(True)
        self.comboBoxAssetName.clear()

        for item in self.assets:
            if item["canceled"]:
                continue            
            self.comboBoxAssetName.addItem(item["name"], userData = item)   


        self.comboBoxAssetName.blockSignals(False)
        self.comboBoxAssetName.setCurrentIndex(0)  

        self.asset_name_changed(self.comboBoxAssetName.currentIndex())                  

    def asset_name_changed(self, index):
        if index < 0:
            return False

        asset = self.get_asset()

        file_list = []
        for item in gazu.files.all_output_files_for_entity(asset):
            file_list.append(item)

        for item in gazu.files.get_all_working_files_for_entity(asset):
            file_list.append(item)

        shared_folder = SwingSettings.get_instance().shared_root()
        directory_list = []
        for item in file_list:
            directory_name = item["path"].replace("/mnt/content/productions", shared_folder)
            if os.path.exists(directory_name):
                if not item["path"] in directory_list:
                    directory_list.append(item["path"])

        self.tableViewFile.setModel(FileTableModel(self, file_list))

        self.tableViewFile.setItemDelegateForColumn(0, CheckBoxDelegate())          

        self.tableViewFile.setAlternatingRowColors(True)
        self.tableViewFile.setColumnWidth(0, 60)
        self.tableViewFile.setColumnWidth(1, 400)
        self.tableViewFile.setColumnWidth(2, 250)

        self.tableViewDir.setModel(DirectoryTableModel(self, directory_list))
        self.tableViewDir.setItemDelegateForColumn(0, CheckBoxDelegate())          

        self.tableViewDir.setAlternatingRowColors(True)
        self.tableViewDir.setColumnWidth(0, 60)
        self.tableViewDir.setColumnWidth(1, 650)


    def select_none(self):
        #for i in range(len(self.shotModel.shots)):
        #    index = self.shotModel.index(i, ShotTableModel.COL_SELECTED)
        #    self.shotModel.setData(index, False, QtCore.Qt.EditRole)     
        pass

    def select_all(self):
        #for i in range(len(self.shotModel.shots)):
        #    index = self.shotModel.index(i, ShotTableModel.COL_SELECTED)
        #    self.shotModel.setData(index, True, QtCore.Qt.EditRole)
        pass

    def get_selected(self):
        #selected = []
        #for i in range(len(self.shotModel.shots)):
        #    if self.shotModel.shots[i]["selected"]:
        #        selected.append(self.shotModel.shots[i])
        #return selected                           
        return False
      
    def close_dialog(self):
        self.write_settings()
        self.close()

    def process(self):
        asset = self.get_asset()
        if not asset:
            return False

        asset_type = self.get_asset_type()

if __name__ == "__main__":
    password = load_keyring('swing', 'password', 'Not A Password')
    
    app = QtWidgets.QApplication(sys.argv)

    dialog = RenameAssetDialog()
    dialog.show()

    sys.exit(app.exec_())
    # wildchildanimation.unreal.gui.swing_sequencer_dialog 
