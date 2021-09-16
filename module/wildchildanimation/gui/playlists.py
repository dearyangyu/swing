# -*- coding: utf-8 -*-

import traceback
import sys
import os
import gazu
import datetime

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

from wildchildanimation.gui.swing_tables import CheckBoxDelegate, human_size, load_file_table_widget

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
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)        

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonProcess.clicked.connect(self.process)
        self.toolButtonSelectFolder.clicked.connect(self.select_output_dir)

        self.model = None
        self.project = None
        self.episode = None
        self.items = []

        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.tableView.doubleClicked.connect(self.table_double_click)

    def load_episode_shot_list(self):
        self.loader = PlaylistLoader(self, self.project, self.episode)
        self.loader.callback.results.connect(self.playlist_loaded)

        self.threadpool.start(self.loader)

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
        for i in self.model._shots:
            item = self.model._shots[i]
            if item["selected"]:
                for t in item["task_type"]:
                    task_type = item["task_type"][t]
                    for shot in task_type["shots"]:
                        print("Checking Shot {} Task Type {}: {}".format(item["name"], t, shot["output_file_name"]))

    def playlist_loaded(self, results):  
        self.items.clear()
        if len(self.task_types) > 0:
            for item in results["items"]:
                if any(item["name"] == x["name"] for x in self.task_types):
                    self.items.append(item)
        else:
            self.items.extend(results)

        self.model = PlaylistModel(self, self.items)
        self.tableView.setModel(self.model)

        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectItems)

        self.tableView.setColumnWidth(0, 20)
        self.tableView.setColumnWidth(1, 175)
        self.tableView.setColumnWidth(2, 180)
        self.tableView.setColumnWidth(3, 50)

        header = self.tableView.horizontalHeader()

        for i in range(3, self.model.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            #self.tableView.setColumnWidth(i, 150)
        #
        
        #self.tableView.setColumnWidth(4, 75)
        self.tableView.verticalHeader().setDefaultSectionSize(self.tableView.verticalHeader().minimumSectionSize())

        checkboxDelegate = CheckBoxDelegate()
        self.tableView.setItemDelegateForColumn(0, checkboxDelegate)  

        editorial_folder = SwingSettings.get_instance().edit_root()

        project = results["project"]
        if "file_tree" in project:
            file_tree = project['file_tree']
            if "editorial" in file_tree:
                mount = file_tree["editorial"]["root"]
                editorial_folder = os.path.normpath(os.path.join(editorial_folder, mount))

        self.lineEditFolder.setText(editorial_folder)      

    def set_selection(self, project, episode):
        self.project = project
        self.set_episode(episode)

    def set_project_episode(self, project, episode, task_types):
        self.project = project
        self.episode = episode
        self.task_types = task_types

        self.lineEditEpisode.setText("Shot List: {} {}".format(self.project["project"], self.episode["episode"]))

        loader = PlaylistLoader(self, self.project["project_id"], self.episode["episode_id"])
        loader.callback.loaded.connect(self.playlist_loaded)
        loader.run()

    def select_output_dir(self):
        working_dir = self.lineEditFolder.text()
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Media Directory", working_dir)
        if q:
            self.lineEditFolder.setText(q)

        

class PlaylistModel(QtCore.QAbstractTableModel):

    columns = [
        "", "Shot", "Last Updated", "Status"
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
                        "selected": True,
                        "status": "",
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
                if section < len(self.columns):
                    return self.columns[section]

                index = section - len(self.columns)
                if index < len(self._task_types):
                    return self._task_types[index].upper()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            item = self.items[index.row()]
            shot = self._shots[item]

            col = index.column()
            if col == 0:
                return shot["selected"]
            elif col == 1:
                return shot["name"]
            elif col == 2:
                last_updated = None
                for t in shot["task_type"]:
                    for s in shot["task_type"][t]["shots"]:
                        if last_updated is None or last_updated < s["updated_at"]:
                            last_updated = s["updated_at"]

                return last_updated
            elif col == 3:
                return shot["status"]
            else:
                indx = col - len(self.columns)
                if indx < len(self._task_types):
                    task_type_name = self._task_types[indx]
                    if task_type_name in shot["task_type"]:
                        layer = shot["task_type"][task_type_name]
                        for item in layer["shots"]:
                            return item["output_file_name"]


    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            col = index.column()
            row = index.row()
            item = self.items[row]  
            shot = self._shots[item] 

            if col == 0:
                if type(value) is bool:
                    shot["selected"] = value
                return True
            elif col == 3:
                shot["status"] = value
                return True
        return False                

    def rowCount(self, index):
        #item = self.items[index.row()]
        #shot = self._shots[item]

        #return shot["index"]
        return len(self.items)   

