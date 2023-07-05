# -*- coding: utf-8 -*-
# Asset Library to sync assets from Treehouse to local storage
# 

import traceback
import sys
import os
import gazu
import datetime
import opentimelineio as otio
import io
import re

import xml.etree.ElementTree as ET

# Qt High DPI 
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

# === theme it dark
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2.QtCore import Signal as pyqtSignal    
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtCore import pyqtSignal    
    qtMode = 1

from datetime import datetime

from wildchildanimation.gui.background_workers import FileDownloader
from wildchildanimation.studio.swing_studio_handler import *
from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.asset_library_dialog import Ui_AssetLibraryDialog

'''
    Swing Asset Library
    ################################################################################
'''

class AssetLibraryDialog(QtWidgets.QDialog, Ui_AssetLibraryDialog):

    def __init__(self, parent = None):
        super(AssetLibraryDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.read_settings()    

        self.pushButtonCancel.clicked.connect(self.close_dialog)     

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)   
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)

        self.toolButtonLibraryFolder.clicked.connect(self.select_library_path)

        self.pushButtonRunAll.clicked.connect(self.download_selected)

        self.threadpool = QtCore.QThreadPool()
        self.threadpool.setMaxThreadCount(3)        

        self.load_project_data()    

    def set_enabled(self, is_enabled):
        self.pushButtonCancel.setEnabled(is_enabled)
        self.pushButtonRunAll.setEnabled(is_enabled)
        self.comboBoxProject.setEnabled(is_enabled)
        self.comboBoxEpisode.setEnabled(is_enabled)
        self.toolButtonLibraryFolder.setEnabled(is_enabled)
        self.lineEditLibraryFolder.setEnabled(is_enabled)

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings("WCA", self.__class__.__name__)
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("library_path", self.lineEditLibraryFolder.text())
        self.settings.setValue("flatten_path", self.checkBoxFlattenPath.isChecked())

        self.settings.endGroup()
        self.settings.sync()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings("WCA", self.__class__.__name__)
        self.settings.beginGroup(self.__class__.__name__)
        
        self.project_root = self.settings.value("projects_root", os.path.expanduser("~"))
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        self.checkBoxFlattenPath.setChecked(self.is_setting_selected(self.settings, "flatten_path"))
        self.lineEditLibraryFolder.setText(self.settings.value("library_path", SwingSettings.get_instance().swing_root()))

    def is_setting_selected(self, settings, value):
        val = settings.value(value, True)
        return val == 'true'        

    def close_dialog(self):
        self.write_settings()
        self.close()        

    def load_project_data(self):
        connect_to_server(SwingSettings.get_instance().swing_user(), SwingSettings.get_instance().swing_password())

        self.projects = gazu.project.all_open_projects()

        self.comboBoxProject.blockSignals(True)
        self.comboBoxProject.clear()

        for item in self.projects:
            self.comboBoxProject.addItem(item["name"], userData = item)
        self.comboBoxProject.blockSignals(False)

        if len(self.projects) > 0:
            self.project_changed(self.comboBoxProject.currentIndex())    

    def select_library_path(self):
        file_name = self.lineEditLibraryFolder.text()
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Library Folder", file_name)
        if q:
            self.lineEditLibraryFolder.setText(q)            

    def project_changed(self, index):
        self.set_enabled(False)
        self.project = self.comboBoxProject.itemData(index)

        if not self.project:
            write_log("Error: No open project could be loaded, please check settings")
            write_log("Server: {}".format(SwingSettings.get_instance().swing_server()))
            write_log("Artist: {}".format(SwingSettings.get_instance().swing_user()))

            return False
        
        self.episodes = gazu.shot.all_episodes_for_project(self.project)

        self.comboBoxEpisode.blockSignals(True)
        self.comboBoxEpisode.clear()

        for item in self.episodes:
            self.comboBoxEpisode.addItem(item["name"], userData = item)
        self.comboBoxEpisode.blockSignals(False)

        if len(self.episodes) > 0:
            self.episode_changed(self.comboBoxEpisode.currentIndex())
        self.set_enabled(True)

    def get_episode_asset_casting(self, asset_type, asset_list):
        assets = []

        for asset in asset_list:
            for item in self.episode_casting:
                if asset["id"] == item["asset_id"]:
                    assets.append(asset)

        return assets

        
    def episode_changed(self, index):
        self.set_enabled(False)
        self.episode = self.comboBoxEpisode.itemData(index)
        self.asset_types = gazu.asset.all_asset_types_for_project(self.project)

        # load casting for episode
        path = F"/data/projects/{self.project['id']}/entities/{self.episode['id']}/casting"
        self.episode_casting = gazu.client.get(path)    

        self.asset_list = gazu.asset.all_assets_for_project(self.project)

        self.treeWidget.clear()

        self.treeWidget.setColumnCount(5)
        self.treeWidget.setHeaderLabels(["", "Name", "Revision", "Updated", "Status"])

        self.treeWidget.setColumnWidth(0, 100)
        self.treeWidget.setColumnWidth(1, 300)
        self.treeWidget.setColumnWidth(2, 100)
        self.treeWidget.setColumnWidth(3, 200)
        self.treeWidget.setColumnWidth(4, 100)

        for asset_type in self.asset_types:
            asset_type_item = QtWidgets.QTreeWidgetItem(self.treeWidget, [ "", asset_type["name"] ])  

            assets = gazu.asset.all_assets_for_project_and_type(self.project, asset_type)

            for asset in self.get_episode_asset_casting(asset_type, assets):
                asset_item = QtWidgets.QTreeWidgetItem(asset_type_item, [ "", asset["name"] ]) 

                working_files = gazu.files.get_all_working_files_for_entity(asset)
                working_files = sorted(working_files, key=lambda x: x["updated_at"], reverse=True)

                selected = False
                for wf in working_files:
                    wf_item = QtWidgets.QTreeWidgetItem(asset_item, [ "", wf["name"], str(wf["revision"]), wf["updated_at"] ]) 
                    wf_item.setData(0, QtCore.Qt.UserRole, wf)

                    wf_item.setFlags(wf_item.flags() | QtCore.Qt.ItemIsUserCheckable)  # Add ItemIsUserCheckable flag

                    if not selected:
                        wf_item.setCheckState(0, QtCore.Qt.Checked)  # Set initial check state                    
                        selected = True
                    else:
                        wf_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set initial check state   

        self.treeWidget.expandAll()
        self.set_enabled(True)                 


    def download_selected(self):
        self.set_enabled(False)

        # Iterate through all items
        root_item = self.treeWidget.invisibleRootItem()  # Get the top-level items

        for index in range(root_item.childCount()):
            item = root_item.child(index)        
            self.iterate_tree_items(item.text(1), item)     

        self.set_enabled(True)

    def iterate_tree_items(self, name, item):
        for index in range(item.childCount()):
            child_item = item.child(index)

            wf = child_item.data(0, QtCore.Qt.UserRole)
            if (wf):
                if child_item.checkState(0) == QtCore.Qt.Checked:
                    self.process_download(child_item, episode_name = self.episode["name"], asset_type_name = name, working_file = wf)
                    print(F"Asset Type: {name}, Asset: {item.text(1)}, Working File: {wf['name']} - Revision: {wf['revision']} [Last Updated {wf['updated_at']}]")

            # Process the child_item as needed
            ## print(child_item.text(0))  # Example: Print the text of the item
            self.iterate_tree_items(name, child_item)  # Recursively iterate child_item's children

    # def update_tracking_sheet(self, sheet_name):

    def process_download(self, tree_item, episode_name, asset_type_name, working_file):
        edit_api = "{}/edit".format(SwingSettings.get_instance().swing_server())
        working_dir = self.lineEditLibraryFolder.text()

        working_file["file_name"] = working_file["name"]

        url = "{}/api/working_file/{}".format(edit_api, working_file["id"])

        if not self.checkBoxFlattenPath.isChecked():
            working_file = set_target(working_file, working_dir)
        else:
            working_file["target_path"] = os.path.join(os.path.normpath(self.lineEditLibraryFolder.text()), episode_name, asset_type_name, working_file["file_name"])

        worker = FileDownloader(self, working_file["id"], url, working_file["target_path"], True, True)
        self.threadpool.start(worker)

        tree_item.setText(4, "Synced")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    if darkStyle:
        # setup stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet())
        # or in new API
        ## app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))      

    test = AssetLibraryDialog(None)
    test.show()

    sys.exit(app.exec_())