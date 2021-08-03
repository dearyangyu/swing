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
        self.sequences = None
        self.items = None

        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.tableView.doubleClicked.connect(self.table_double_click)

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

    def set_episode(self, episode):
        self.episode = episode

        self.comboBoxSequence.clear()
        self.comboBoxSequence.setEnabled(False)

        if self.episode:
            self.sequences = self.episode["sequences"]
            for item in self.sequences:
                self.comboBoxSequence.addItem(item["name"])
                self.comboBoxSequence.setEnabled(True)                

        loader = PlaylistLoader(self, self.project, self.episode)
        loader.callback.results.connect(self.playlist_loaded)
        loader.run()

        

class PlaylistModel(QtCore.QAbstractTableModel):

    columns = [
        "Name", "For", 
    ]    

    def __init__(self, parent, playlists = None):
        super(PlaylistModel, self).__init__(parent)
        self.items = []
        if playlists:
            for item in playlists:
                self.items.append(item)

    def flags(self, index):
        col = index.column()
        if col in [0, 3, 4, 5]:
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
            item = self.items[index.row()]

            col = index.column()
            if 0 == col:
                return item["name"]
            elif 1 == col:
                if "for_entity" in item:
                    return item["for_entity"]
            elif 2 == col:
                if "project_file_name" in item:
                    return item["project_file_name"]
            elif 3 == col:
                return item["nb_frames"]
            elif 4 == col:
                return item["in"]
            elif 5 == col:
                return item["out"]
            elif 6 == col:
                return item["status"]

    def rowCount(self, index):
        return len(self.items)   

