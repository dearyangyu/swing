# -*- coding: utf-8 -*-

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

from datetime import datetime

import wildchildanimation.gui.background_workers as bg
from wildchildanimation.gui.swing_utils import *

from wildchildanimation.gui.references_dialog import Ui_ReferencesDialog

from wildchildanimation.gui.swing_tables import human_size
from wildchildanimation.gui.downloads import *

TEST_MISSING = [
    'C:/Users/wildwrangler/Documents/maya/projects/hushabye_s02/hsb2_build/e00/shots/sq00/sh00/layout/sq00_sh00_layout/hby_e00_sq00_sh00_layout.mb',
    'C:/Users/wildwrangler/Documents/maya/projects/hushabye_s02/hsb2_build/e00/shots/sq00/cloud_test/layout/sq00_cloud_test_layout/hby_BBC_Test_v01.ma',
    'C:/Users/wildwrangler/Documents/maya/projects/hushabye_s02/hsb2_build/e00/shots/sq00/cloud_test/layout/sq00_cloud_test_layout/hby_BBC_Test_v01.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_dillyDally_rig_v004.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_mountains_master_02.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_launchpad_mastermesh_02.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_wall_mastermesh_02.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_rocket_mastermesh.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_dillyTeddy_rig_v002.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_titleText_mastermesh.ma',
    '/Volumes/LaCie 12big USB3.1/user/jen/HB2/season_02/layout_main/assets/props/hushabye_season_2_prop_bed_asset_model_v3.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hushabye_season_2_environment_mountains_hills_model_v4.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_prop_cloud_proxy_v001.ma',
    'C:/Users/wildwrangler/Documents/maya/projects/hushabye_s02/hsb2_build/e00/shots/sq00/cloud_test/layout/sq00_cloud_test_layout/hby_BBC_Test_v01.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_dillyDally_rig_v004.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_mountains_master_02.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_launchpad_mastermesh_02.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_wall_mastermesh_02.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_rocket_mastermesh.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_dillyTeddy_rig_v002.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_titleText_mastermesh.ma{1}',
    '/Volumes/LaCie 12big USB3.1/user/jen/HB2/season_02/layout_main/assets/props/hushabye_season_2_prop_bed_asset_model_v3.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hushabye_season_2_environment_mountains_hills_model_v4.ma{1}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{5}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{5}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_prop_cloud_proxy_v001.ma{1}',
    'C:/Users/wildwrangler/Documents/maya/projects/hushabye_s02/hsb2_build/e00/shots/sq00/cloud_test/layout/sq00_cloud_test_layout/hby_BBC_Test_v01.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_dillyDally_rig_v004.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_mountains_master_02.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_launchpad_mastermesh_02.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_wall_mastermesh_02.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_rocket_mastermesh.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_dillyTeddy_rig_v002.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_titleText_mastermesh.ma{2}',
    '/Volumes/LaCie 12big USB3.1/user/jen/HB2/season_02/layout_main/assets/props/hushabye_season_2_prop_bed_asset_model_v3.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hushabye_season_2_environment_mountains_hills_model_v4.ma{2}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{6}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{6}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{7}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{8}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{7}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{8}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_prop_cloud_proxy_v001.ma{2}',
    'C:/Users/wildwrangler/Documents/maya/projects/hushabye_s02/hsb2_build/e00/shots/sq00/cloud_test/layout/sq00_cloud_test_layout/hby_BBC_Test_v01.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_dillyDally_rig_v004.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_mountains_master_02.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_launchpad_mastermesh_02.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_wall_mastermesh_02.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_rocket_mastermesh.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_dillyTeddy_rig_v002.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_titleText_mastermesh.ma{3}',
    '/Volumes/LaCie 12big USB3.1/user/jen/HB2/season_02/layout_main/assets/props/hushabye_season_2_prop_bed_asset_model_v3.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hushabye_season_2_environment_mountains_hills_model_v4.ma{3}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{9}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{9}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{10}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{11}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{10}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{11}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_prop_cloud_proxy_v001.ma{3}',
    'C:/Users/wildwrangler/Documents/maya/projects/hushabye_s02/hsb2_build/e00/shots/sq00/cloud_test/layout/sq00_cloud_test_layout/hby_BBC_Test_v01.ma{5}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_dillyDally_rig_v004.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_mountains_master_02.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_launchpad_mastermesh_02.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_wall_mastermesh_02.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_rocket_mastermesh.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_dillyTeddy_rig_v002.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hby_titleText_mastermesh.ma{4}',
    '/Volumes/LaCie 12big USB3.1/user/jen/HB2/season_02/layout_main/assets/props/hushabye_season_2_prop_bed_asset_model_v3.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/environments/hushabye_season_2_environment_mountains_hills_model_v4.ma{4}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{12}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{12}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{13}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_rig_v003.ma{14}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{13}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/characters/hby_character_flower_small_rig_v003.ma{14}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_prop_cloud_proxy_v001.ma{4}'
]


class ReferencesDialogGUI(QtWidgets.QDialog, Ui_ReferencesDialog):

    working_dir = None
    
    def __init__(self, parent = None, handler = None, entity = None, task_types = None):
        super(ReferencesDialogGUI, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(640)

        self.handler = handler
        self.entity = entity
        self.task_types = task_types

        if self.handler:
            self.files = self.handler.list_unresolved()
            write_log("[swing]", "Loaded {0} files from Maya".format(len(self.files)))
        else:
            self.files = TEST_MISSING
            write_log("[swing]", "Loaded {0} TEST FILES".format(len(self.files)))

        self.threadpool = QtCore.QThreadPool.globalInstance()

        loader = bg.EntityLoaderThread(self, self.entity["id"])
        loader.callback.loaded.connect(self.entity_loaded)
        self.threadpool.start(loader)        

        self.pushButtonDownload.clicked.connect(self.process)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        self.toolButtonAll.clicked.connect(self.select_all)
        self.toolButtonNone.clicked.connect(self.select_none)

        self.setWorkingDir(load_settings("projects_root", os.path.expanduser("~")))

    def process(self):
        #self.threadpool = QtCore.QThreadPool()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://example.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        file_list = []

        self.counter = 0
        while self.counter < self.tableWidget.rowCount():
            row_item = self.tableWidget.item(self.counter, 0)
            if row_item.checkState():
                file_list.append(row_item.data(QtCore.Qt.UserRole))

            self.counter += 1

        worker = bg.SearchFn(self, edit_api, email, password, file_list)
        worker.callback.results.connect(self.search_results)

        self.threadpool.start(worker)

        self.enable_ui(False)
        #worker.run()
    # process        

    def enable_ui(self, enabled):
        self.pushButtonDownload.setEnabled(enabled)
        self.pushButtonCancel.setEnabled(enabled)
        self.toolButtonAll.setEnabled(enabled)
        self.toolButtonNone.setEnabled(enabled)

        if enabled:
            self.progressBar.setRange(0, 1)
        else:
            # set progressbar to busy
            self.progressBar.setRange(0, 0)

    def search_results(self, results):
        self.enable_ui(True)

        file_list = []

        for sr in results:
            for result in sr:
                file_list.append(result)

        dialog = DownloadDialogGUI(self, self.entity, self.task_types, file_list)
        dialog.load_files(file_list)
        dialog.resize(self.size())
        dialog.exec_()            

        self.hide()

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

    def setWorkingDir(self, working_dir):
        self.working_dir = working_dir

    def close_dialog(self):
        self.close()     

    def entity_loaded(self, data):
        self.type = data["type"]
        self.project = data["project"]

        sections = []
        if self.type == "Shot":
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
            sections.append(self.entity["name"].strip())

        namespace = "_".join(sections).lower().strip()

        load_table_widget(self.tableWidget, self.files)
        self.setEnabled(True)


def load_table_widget(tableWidget, files):
    model = []

    unique_files = []
    for item in files:
        item_name = item.split("{")[0]
        if not item_name in unique_files:
            unique_files.append(item_name)
    
    for item in unique_files:
        name, ext = os.path.splitext(os.path.basename(item))

        model.append({
            "name": os.path.basename(item),
            "item": item,
            "filename": name,
            "fileext": ext,
            "size": "0",
            "status": "unknown"
        })

    tableWidget.setRowCount(len(model))

    row = 0
    for item in model:
        cell = QtWidgets.QTableWidgetItem(item["name"])
        cell.setData(QtCore.Qt.UserRole, item)

        cell.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        cell.setCheckState(QtCore.Qt.Checked)  
        tableWidget.setItem(row, 0, cell)

        row += 1

    return tableWidget
###########################################################################           
