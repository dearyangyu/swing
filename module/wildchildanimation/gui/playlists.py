# -*- coding: utf-8 -*-

import traceback
import sys
import os
import gazu
import json
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

from wildchildanimation.gui.swing_tables import CheckBoxDelegate, human_size

from wildchildanimation.gui.playlist_loader import *
from wildchildanimation.gui.playlist_worker import *

'''
    PlaylistDialog class
    ################################################################################
'''

class PlaylistDialog(QtWidgets.QDialog, Ui_PlaylistDialog):

    working_dir = None
    
    def __init__(self, parent = None):
        super(PlaylistDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)        

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonProcess.clicked.connect(self.process)
        self.toolButtonSelectFolder.clicked.connect(self.select_output_dir)
        self.toolButtonRefresh.clicked.connect(self.refresh_playlists)

        self.model = None
        self.project = None
        self.episode = None
        self.items = []
        self.count = len(self.items)

        self.radioButtonLatestVersion.setChecked(True)
        self.radioButtonLatestVersion.clicked.connect(self.update_tree)
        self.radioButtonLastDay.clicked.connect(self.update_tree)
        self.radioButtonShowAll.clicked.connect(self.update_tree)

        self.threadpool = QtCore.QThreadPool.globalInstance()

        set_button_icon(self.toolButtonSelectAll, "../resources/fa-free/solid/plus.svg")
        self.toolButtonSelectAll.clicked.connect(self.select_all)

        self.toolButtonSelectNone.clicked.connect(self.select_none)
        set_button_icon(self.toolButtonSelectNone, "../resources/fa-free/solid/minus.svg")

        self.tableView.doubleClicked.connect(self.file_table_double_click)


    def load_episode_shot_list(self):
        self.loader = PlaylistLoader(self, self.project, self.episode)
        self.loader.callback.results.connect(self.playlist_loaded)

        self.threadpool.start(self.loader)

    def set_project(self, project):
        self.project = project
        
    def close_dialog(self):
        self.close()        

    def select_all(self):
        self.model.select_all()
        self.tableView.update()        

    def select_none(self):
        self.model.select_none()
        self.tableView.update()        

    def file_table_double_click(self, index):
        self.selected_file = self.tableView.model().data(index, QtCore.Qt.UserRole)        
        if self.selected_file:

            output_dir = "{}/{}".format(self.lineEditFolder.text(), self.episode["name"])
            file_path = os.path.join(output_dir, self.selected_file["output_file_name"])

            if os.path.isfile(file_path):
                reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(os.path.dirname(file_path))
                    return True        

    def process(self):   
        model = self.tableView.model()
        self.count = 0 
        for x in range(model.rowCount()):
            item = model.data(model.index(x, 0), QtCore.Qt.UserRole)
            item["model_index"] = x

            if not item["selected"]:
                continue

            worker = PlaylistWorker(self, item, target = self.lineEditFolder.text(), skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZip.isChecked())
            worker.callback.progress.connect(self.update_progress)
            worker.callback.done.connect(self.update_done)
            
            self.count += 1
            self.threadpool.start(worker)
            #worker.run()

        self.progressBar.setMaximum(self.count)

    def update_progress(self, status):
        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            item = self.tableView.model().data(index, QtCore.Qt.UserRole)

            if status["file_id"] == item['output_file_id']:
                index = self.tableView.model().index(row, PlaylistModel.COL_STATUS)

                mesg = status["message"]
                if "size" in status:
                    mesg = "{} {}".format(mesg, human_size(status["size"]))

                self.tableView.model().setData(index, mesg, QtCore.Qt.EditRole) 
                self.tableView.model().dataChanged.emit(index, index, QtCore.Qt.DisplayRole)           
                self.tableView.viewport().update()     
                break

    def update_done(self, status):
        if "item" in status:
            item = status["item"]
            mesg = status["message"]

            for row in range(self.tableView.model().rowCount()):
                index = self.tableView.model().index(row, 0)
                shot = self.tableView.model().data(index, QtCore.Qt.UserRole)
                if item["output_file_id"] == shot['output_file_id']:

                    index = self.tableView.model().index(row, PlaylistModel.COL_STATUS)

                    self.tableView.model().setData(index, mesg, QtCore.Qt.EditRole) 
                    self.tableView.model().dataChanged.emit(index, index, QtCore.Qt.DisplayRole)           
                    self.tableView.viewport().update()    
                    break       
        else:
            for row in range(self.tableView.model().rowCount()):
                index = self.tableView.model().index(row, 0)
                shot = self.tableView.model().data(index, QtCore.Qt.UserRole)
                if status["file_id"] == shot['output_file_id']:

                    index = self.tableView.model().index(row, PlaylistModel.COL_STATUS)

                    self.tableView.model().setData(index, status["message"], QtCore.Qt.EditRole) 
                    self.tableView.model().dataChanged.emit(index, index, QtCore.Qt.DisplayRole)           
                    self.tableView.viewport().update()    
                    break 

        self.count -= 1
        if self.count < self.progressBar.maximum():
            self.progressBar.setValue(self.progressBar.maximum()- self.count)
        #print("{} {}".format(self.count, self.progressBar.maximum()))

    def playlist_loaded(self, results):  
        self.items.clear()
        if len(self.task_types) > 0:
            for item in results["items"]:
                if any(item["name"] == x["name"] for x in self.task_types):
                    self.items.append(item)
        else:
            self.items.extend(results)

        self.project = results["project"]
        self.episode = results["episode"]
        self.lineEditEpisode.setText("Shot List: {} {}".format(self.project["name"], self.episode["name"]))

        self.update_tree()
        editorial_folder = SwingSettings.get_instance().edit_root()

        if "file_tree" in self.project:
            file_tree = self.project['file_tree']
            if "editorial" in file_tree:
                mount = file_tree["editorial"]["mountpoint"]
                mount = mount.replace("/mnt/content/productions", editorial_folder)
                editorial_folder = os.path.normpath(os.path.join(mount, file_tree["editorial"]["root"]))

        self.lineEditFolder.setText(editorial_folder)      

    def set_selection(self, project, episode):
        self.project = project
        self.set_episode(episode)

    def set_project_episode(self, project_id, episode_id, task_types):
        self.project_id = project_id
        self.episode_id = episode_id
        self.task_types = task_types

        self.refresh_playlists()

    def refresh_playlists(self):
        loader = PlaylistLoader(self, self.project_id, self.episode_id)
        loader.callback.loaded.connect(self.playlist_loaded)
        loader.run()

    def select_output_dir(self):
        working_dir = self.lineEditFolder.text()
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Media Directory", working_dir)
        if q:
            self.lineEditFolder.setText(q)


    def update_tree(self):
        mode = ""
        if self.radioButtonShowAll.isChecked():
            mode = "all"
        elif self.radioButtonLastDay.isChecked():
            mode = "last_day"
        elif self.radioButtonLatestVersion.isChecked():
            mode = "latest_version"

        self.model = PlaylistModel(self.items, self.task_types, parent = None, mode = mode)

        proxy = QtCore.QSortFilterProxyModel()
        proxy.setSourceModel(self.model)
        proxy.setDynamicSortFilter(True)

        self.tableView.setModel(proxy)

        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)

        self.tableView.sortByColumn(PlaylistModel.COL_SHOT, QtCore.Qt.AscendingOrder)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.tableView.setColumnWidth(PlaylistModel.COL_SELECT, 40)
        self.tableView.setColumnWidth(PlaylistModel.COL_SHOT, 225)
        self.tableView.setColumnWidth(PlaylistModel.COL_TASK, 160)
        self.tableView.setColumnWidth(PlaylistModel.COL_NAME, 260)
        self.tableView.setColumnWidth(PlaylistModel.COL_VERSION, 75)
        self.tableView.setColumnWidth(PlaylistModel.COL_UPDATED, 180)
        self.tableView.setColumnWidth(PlaylistModel.COL_STATUS, 150)

        checkboxDelegate = CheckBoxDelegate()
        self.tableView.setItemDelegateForColumn(0, checkboxDelegate)  
        return True

class PlaylistModel(QtCore.QAbstractTableModel):

    COLUMNS = ["", "Shot", "Task", "Version", "Name", "Updated", "Status" ]
    items = []

    COL_SELECT = 0
    COL_SHOT = 1
    COL_TASK = 2
    COL_VERSION = 3
    COL_NAME = 4
    COL_UPDATED = 5
    COL_STATUS = 6

    def __init__(self, data, task_types, parent = None, mode = "show_all"):
        super(PlaylistModel, self).__init__(parent)

        self.task_type_dict = {}
        for item in task_types:
            self.task_type_dict[item["name"]] = item

        self.loadModelData(data, mode)

    def select_all(self):
        for i in self.items:
            i["selected"] = True
        self.dataChanged.emit(0, len(self.items))

    def select_none(self):
        for i in self.items:
            i["selected"] = False
        self.dataChanged.emit(0, len(self.items))


    def loadModelData(self, playlists, mode):
        _shots = {}
        _items = []
        _task_types = {}

        for item in playlists:
            shot_name = "{} {} {}".format(item["ep"], item["sq"], item["sh"]).lower()

            if shot_name in _shots:
                shot = _shots[shot_name]
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
                    "task_type": self.task_type_dict[task_type_name],
                    "shots": []
                }

            # save priority for sorting
            if not task_type_name in _task_types:
                _task_types[task_type_name] = item["priority"]

            layer["shots"].append(item)
            shot["task_type"][task_type_name] = layer
            shot["index"] += 1                
            _shots[shot_name] = shot

        _items = list(_shots.keys())
        _items.sort()

        # sort task types by prio
        _task_types = sorted(_task_types, key = lambda x: _task_types[x], reverse=True)

        now = datetime.now()        

        latest_versions = []

        self.items.clear()
        for shot_name in _items:
            shot = _shots[shot_name]

            if "latest_version" in mode and shot_name in latest_versions:
                continue

            for col in range(len(_task_types)):
                col_header = _task_types[col]
                if col_header in shot["task_type"]:
                    shots = shot["task_type"][col_header]["shots"]

                    # sort by latest shot
                    shots = sorted(shots, key = lambda x: x["updated_at"])

                    revision = len(shots)

                    for sh in shots:
                        sh["shot_name"] = shot_name
                        sh["selected"] = True
                        sh["status"] = ""
                        sh["version"] = revision
                        revision -= 1                        

                        # if we are not showing all shots, only show latest version
                        # and update header row

                        if "latest_version" in mode:
                            if not shot_name in latest_versions:
                                self.items.append(sh)                                
                                latest_versions.append(shot_name)
                            continue

                        elif "last_day" in mode:
                            updated_at = sh["updated_at"]
                            updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%f')
                            delta = now - updated_at

                            if delta.days <= 1:
                                self.items.append(sh)
                                break
                        else:
                            self.items.append(sh)


    def columnCount(self, parent=QtCore.QModelIndex()):
        return PlaylistModel.COLUMNS.__len__()

    def data(self, index, role):
        if not index.isValid():
            return None

        col_index = index.column()
        row_index = index.row()

        item = self.items[row_index]

        if role == QtCore.Qt.UserRole:
            return item

        if role == QtCore.Qt.ForegroundRole:
            # task type 
            if col_index == PlaylistModel.COL_TASK:
                task_type = item["name"]
                if task_type in self.task_type_dict:
                    tt = self.task_type_dict[task_type]
                    if "color" in tt:
                        return QtGui.QColor(tt["color"])

            elif col_index == PlaylistModel.COL_UPDATED:
                try:
                    updated_at = item["updated_at"]
                    updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%f')
                    now = datetime.now()
                    delta = now - updated_at
                    if delta.days <= 0:
                        return QtGui.QColor("#32cd32") # show new in green
                    #else:
                    #    return QtGui.QColor("#FF0000")
                except:
                    traceback.print_exc()
                    return None

            # date time
            elif col_index == PlaylistModel.COL_STATUS:
                status = item["status"]
                if status == "":
                    return None
                elif "downloading" in status:
                    return QtGui.QColor("#32cd32") # blue
                elif "done" in status:
                    return QtGui.QColor("#0000cd") # green
                elif "skipped" in status:
                    return QtGui.QColor("#ffa500") # orange
                #else:
                #    return QtGui.QColor("#FF0000")
            return None

        elif role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None

        if PlaylistModel.COL_SELECT == col_index:
            return item["selected"] 

        elif PlaylistModel.COL_SHOT == col_index:
            return item["shot_name"]

        elif PlaylistModel.COL_TASK == col_index:
            return item["name"]

        elif PlaylistModel.COL_VERSION == col_index:
            return item["version"]            

        elif PlaylistModel.COL_NAME == col_index:
            return item["output_file_name"]

        elif PlaylistModel.COL_UPDATED == col_index:
            return item["updated_at"]

        elif PlaylistModel.COL_STATUS == col_index:
            return item["status"]

        return None

    def flags(self, index):
        if not index.isValid():
            return 0

        if index.column() == 0:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEditable | super(PlaylistModel, self).flags(index)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return PlaylistModel.COLUMNS[section]

        return None

    def rowCount(self, parent=QtCore.QModelIndex()):

        return len(self.items)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        col_index = index.column()
        row_index = index.row()

        item = self.items[row_index]            
        if PlaylistModel.COL_SELECT == col_index:
            item["selected"] = bool(value)
            self.dataChanged.emit(index, index)
            return True

        elif PlaylistModel.COL_STATUS == col_index:
            item["status"] = str(value)
            self.dataChanged.emit(index, index)
            return True

        return False

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test = PlaylistDialog(None)
    #test = FileSelectDialog(None, "E:/productions/Tom_Gates_Sky_S02/tg_2d_main/tg_2d_build/tg_2d_ep206/shots/sc100/sh010/anim_block/sc100_sh010_anim_block/")

    #test.pushButtonWorkingFiles.setVisible(True)
    #test.pushButtonOutputFiles.setVisible(True)
    #test.pushButtonZip.setVisible(True)


    test.show()
    sys.exit(app.exec_())