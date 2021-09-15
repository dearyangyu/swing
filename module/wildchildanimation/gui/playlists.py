# -*- coding: utf-8 -*-

import traceback
import sys
import os
import re
import json
import gazu

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtCore, QtWidgets
    import sip
    qtMode = 1

from datetime import datetime

from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.playlist_dialog import Ui_PlaylistDialog

from wildchildanimation.gui.swing_tables import human_size, load_file_table_widget

from wildchildanimation.gui.background_workers import ShotCreator, ShotCreatorSignal

from wildchildanimation.gui.media_info import *
from wildchildanimation.gui.playlist_loader import *


'''
    PlaylistDialog class
    ################################################################################
'''

class PlaylistDialog(QtWidgets.QDialog, Ui_PlaylistDialog):

    working_dir = None
    
    def __init__(self, parent = None):
        super(PlaylistDialog, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.pushButtonCancel.clicked.connect(self.close_dialog)

        self.model = None
        self.project = None
        self.episode = None
        self.items = None

        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.tableView.doubleClicked.connect(self.table_double_click)
        self.comboBoxEpisode.currentIndexChanged.connect(self.load_episode_shot_list)


    def load_episode_shot_list(self):
        self.loader = PlaylistLoader(self, self.project, self.episode)
        self.loader.callback.results.connect(self.playlist_loaded)

        self.threadpool.start(self.loader)

    def playlist_loaded(self, results):
        self.items = results

        for i in self.items:
            print(i)

    def set_project(self, project):
        self.project = project
        
    def close_dialog(self):
        self.close()        

    def table_double_click(self, index):
        row_index = index.row()
        self.selected = self.items[row_index]
        if self.selected:
            print(self.selected)
            playlist = gazu.playlist.get_playlist(self.selected)
            shots = gazu.playlist.all_shots_for_playlist(self.selected)
            print(shots)

    def process(self):    
        pass

    def playlist_loaded(self, results):   
        self.items = results

        self.model = PlaylistModel(self, self.items)
        self.tableView.setModel(self.model)

        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectItems)
        self.tableView.setColumnWidth(0, 100)
        self.tableView.setColumnWidth(1, 200)
        self.tableView.setColumnWidth(2, 200)
        self.tableView.setColumnWidth(3, 75)
        self.tableView.setColumnWidth(4, 75)

        self.tableView.verticalHeader().setDefaultSectionSize(self.tableView.verticalHeader().minimumSectionSize())

    def set_selection(self, project, episode):
        self.project = project
        self.set_episode(episode)

    def set_project_episode(self, project, episode):
        self.project = project
        self.episode = episode

        loader = PlaylistLoader(self, self.project["project_id"], self.episode["episode_id"])
        loader.callback.loaded.connect(self.playlist_loaded)
        loader.run()

        

class PlaylistModel(QtCore.QAbstractTableModel):

    columns = [
        "Name", "For", 
    ]   

    _shots = {}
    _items = []
    _task_types = []

    def __init__(self, parent, playlists = None):
        super(PlaylistModel, self).__init__(parent)

        self._shots = {}
        self._items = []
        self._task_types = {}

        if playlists:
            for item in playlists:
                shot_name = "{} {} {}".format(item["ep"], item["sq"], item["sh"])

                if shot_name in self._shots:
                    shot = self._shots[shot_name]
                else:
                    shot = {
                        "name": shot_name,
                        "index": 0,
                        "task_type": {}
                    }


                task_type_name = item["name"]
                if task_type_name in shot["task_type"]:
                    layer = shot["task_type"][task_type_name]
                else:
                    layer = {
                        "name": task_type_name,
                        "shots": []
                    }

                if not task_type_name in self._task_types:
                    self._task_types[task_type_name] = item["priority"]

                layer["shots"].append(item)
                shot["task_type"][task_type_name] = layer
                shot["index"] += 1                
                self._shots[shot_name] = shot

        self.items = list(self._shots.keys())
        self.items.sort()

        self._task_types = sorted(self._task_types, key = lambda x: self._task_types[x])

    def flags(self, index):
        col = index.column()
        if col in [0, 3, 4, 5]:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled| QtCore.Qt.ItemIsEditable            
            
        return QtCore.Qt.ItemIsEnabled

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns) + len(self._task_types)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Shot"
                elif section > 0 and (section - 1) < len(self._task_types):
                    layer_name = self._task_types[section - 1]
                    return layer_name                

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            item = self.items[index.row()]
            shot = self._shots[item]

            col = index.column()
            if col == 0:
                return shot["name"]
            elif col > 0 and (col - 1) < len(self._task_types):
                task_type_name = self._task_types[col - 1]
                if task_type_name in shot["task_type"]:
                    layer = shot["task_type"][task_type_name]
                    for item in layer["shots"]:
                        return item["output_file_name"]

                return ""

    def rowCount(self, index):
        #item = self.items[index.row()]
        #shot = self._shots[item]

        #return shot["index"]
        return len(self.items)   

