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
from shutil import copy2

import tempfile

from wildchildanimation.gui.swing_utils import load_keyring, extract_archive
from wildchildanimation.studio.studio_interface import StudioInterface

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.background_workers import ProjectLoaderThread
from wildchildanimation.gui.swing_utils import connect_to_server
from wildchildanimation.gui.shot_table import ShotTableModel

from wildchildanimation.unreal.gui.asset_selector_widget import Ui_AssetSelectorWidget

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2.QtCore import QThreadPool
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtCore import QThreadPool
    qtMode = 1

class AssetSelectorDialog(QtWidgets.QDialog, Ui_AssetSelectorWidget):

    def __init__(self, parent = None):
        super(AssetSelectorDialog, self).__init__(parent) # Call the inherited classes __init__ method    
        self.setupUi(self)
        self.setWindowTitle("Swing UE Asset Import")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.read_settings()
        self.threadpool = QThreadPool.globalInstance()

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

    def get_fbx_working_file(self):
        return self.comboBoxFBX.currentData()

    def get_texture_working_file(self):
        return self.comboBoxTextures.currentData()

    def is_archive_file(self, file_name):
        fn, ext = os.path.splitext(file_name)

        is_archive = False
        for item in StudioInterface.UNARCHIVE_TYPES:
            if item in ext:
                is_archive = True        

        return is_archive

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
        self.comboBoxFBX.clear()
        self.comboBoxTextures.clear()

        self.project_changed(self.comboBoxProject.currentIndex())

    def project_changed(self, index):
        project = self.comboBoxProject.itemData(index)

        if "project_id" in project:
            project = gazu.project.get_project(project["project_id"])

        self.comboBoxAssetType.clear()
        self.comboBoxAssetName.clear()
        self.comboBoxFBX.clear()
        self.comboBoxTextures.clear()

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

        self.comboBoxFBX.blockSignals(True)
        self.comboBoxTextures.blockSignals(True)

        self.comboBoxFBX.clear()
        self.comboBoxTextures.clear()

        working_files = gazu.files.get_all_working_files_for_entity(asset)

        fbx_id_index = -1
        texture_id_index = -1

        id = 0
        for item in working_files:
            self.comboBoxFBX.addItem(item["name"], userData = item)
            self.comboBoxTextures.addItem(item["name"], userData = item)

            if ".fbx" in item["name"]:
                fbx_id_index = id

            # any(x == 'Erik' for x in ['Erik', 'John', 'Jane', 'Jim'])
            if any(x in item["name"] for x in [ "Textures", "Tx" ]):
                texture_id_index = id

            id += 1

        if fbx_id_index >= 0:
            self.comboBoxFBX.setCurrentIndex(fbx_id_index)

        if texture_id_index >= 0:
            self.comboBoxTextures.setCurrentIndex(texture_id_index)

        self.comboBoxFBX.blockSignals(False)
        self.comboBoxTextures.blockSignals(False)

    def select_none(self):
        for i in range(len(self.shotModel.shots)):
            index = self.shotModel.index(i, ShotTableModel.COL_SELECTED)
            self.shotModel.setData(index, False, QtCore.Qt.EditRole)     

    def select_all(self):
        for i in range(len(self.shotModel.shots)):
            index = self.shotModel.index(i, ShotTableModel.COL_SELECTED)
            self.shotModel.setData(index, True, QtCore.Qt.EditRole)

    def get_selected(self):
        selected = []
        for i in range(len(self.shotModel.shots)):
            if self.shotModel.shots[i]["selected"]:
                selected.append(self.shotModel.shots[i])
        return selected                           
      
    def close_dialog(self):
        self.write_settings()
        self.close()

    def process(self):
        asset = self.get_asset()
        if not asset:
            return False

        asset_type = self.get_asset_type()

        fbx_working_file = self.get_fbx_working_file()
        texture_working_file = self.get_texture_working_file()

        fbx_dirs = []
        texture_dirs = []

        if fbx_working_file:
            target_dir = fbx_working_file["path"].replace("/mnt/content/productions", SwingSettings.get_instance().swing_root())

            source = os.path.join(fbx_working_file["path"], fbx_working_file["name"]).replace("/mnt/content/productions", SwingSettings.get_instance().shared_root())

            target_dir = os.path.join(target_dir, "components")
            os.makedirs(target_dir, exist_ok=True)

            if os.path.exists(source):
                print("Copying {} to {}".format(source, target_dir))
                copy2(source, target_dir)

            fbx_dirs.append(target_dir)

        if texture_working_file:
            target_dir = texture_working_file["path"].replace("/mnt/content/productions", SwingSettings.get_instance().swing_root())
            source = os.path.join(texture_working_file["path"], texture_working_file["name"]).replace("/mnt/content/productions", SwingSettings.get_instance().shared_root())        

            target_dir = os.path.join(target_dir, "textures")
            os.makedirs(target_dir, exist_ok=True)

            if os.path.exists(source):
                if self.is_archive_file(texture_working_file["name"]):
                    extract_mode = 'e'

                    if '.zip' in source:
                        extract_mode = 'x'                    
                    
                    if extract_archive(SwingSettings.get_instance().bin_7z(), source, target_dir, extract_mode = extract_mode):
                        print("Extracted archive")

                    texture_dirs.append(target_dir)

                else:
                    print("Copying {} to {}".format(source, target_dir))
                    copy2(source, target_dir)
                    texture_dirs.append(target_dir)

        # now we have the asset name, all fbx files and all textures uploaded
        # need to pass this to unreal to import / create 



if __name__ == "__main__":
    password = load_keyring('swing', 'password', 'Not A Password')
    
    app = QtWidgets.QApplication(sys.argv)

    dialog = AssetSelectorDialog()
    dialog.show()

    sys.exit(app.exec_())
    # wildchildanimation.unreal.gui.swing_sequencer_dialog 
