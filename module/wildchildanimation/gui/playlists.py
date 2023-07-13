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
    from PyQt5 import QtCore, QtWidgets
    import sip
    qtMode = 1

from datetime import datetime

from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.playlist_dialog import Ui_PlaylistDialog

from wildchildanimation.gui.swing_tables import CheckBoxDelegate, human_size

from wildchildanimation.gui.playlist_loader import *
from wildchildanimation.gui.playlist_worker import *

# import opentimelineio as otio

import json

'''
    PlaylistDialog class
    ################################################################################
'''

class PlaylistDialog(QtWidgets.QDialog, Ui_PlaylistDialog):

    PLAYLIST_FILE = "swing-playlist.json"
    INVALID_FILE_TYPES = [".elementTable", ".versionTable", ".aux", ".aux~", ".xstage", ".xstage~", ".ma", ".mb", ".zip", ".7z" ]

    working_dir = None
    
    def __init__(self, parent = None):
        super(PlaylistDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        self.read_settings()        

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
        self.checkBoxSequences.clicked.connect(self.update_tree)

        self.lineEditSearch.textChanged.connect(self.search)
        self._createContextMenu()

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("show_sequences", self.checkBoxSequences.isChecked())
        self.settings.setValue("extract_zip", self.checkBoxExtractZip.isChecked())

        #self.settings.setValue("software", self.comboBoxSoftware.currentText())

        #self.settings.setValue("output_dir_path_le", self.output_dir_path_le.text())
        #self.settings.setValue("output_filename_le", self.output_filename_le.text())
        
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.project_root = self.settings.value("projects_root", os.path.expanduser("~"))
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))

        self.checkBoxSequences.setChecked(self.is_setting_selected(self.settings, "show_sequences"))
        self.checkBoxExtractZip.setChecked(self.is_setting_selected(self.settings, "extract_zip"))     

        ##self.move(self.settings.value("pos", QtCore.QPoint(0, 200)))
        self.settings.endGroup()        

    def is_setting_selected(self, settings, value):
        val = settings.value(value, True)
        return val == 'true'        

    def search(self):
        text = self.lineEditSearch.text()
        if len(text) and self.proxy:
            self.proxy.setFilterFixedString(text)

    def load_episode_shot_list(self):
        self.loader = PlaylistLoader(self, self.project, self.episode)
        self.loader.callback.results.connect(self.playlist_loaded)

        self.threadpool.start(self.loader)

    def set_project(self, project):
        self.project = project
        
    def close_dialog(self):
        self.write_settings()
        self.close()        

    def select_all(self):
        self.model.select_all()
        self.tableView.update()        

    def select_none(self):
        self.model.select_none()
        self.tableView.update()     

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

    def file_table_double_click(self, index):
        self.filesOpenDirectory()

    def _createContextMenu(self):
        # File actions
        self.actionViewKitsu = self._loadActionIcon("&View in Kitsu", "../resources/fa-free/solid/info-circle.svg")
        self.actionViewKitsu.setStatusTip("Open Shot in Kitsu")
        self.actionViewKitsu.triggered.connect(self.viewInKitsu)

        self.actionOpenDirectory = self._loadActionIcon("&Open Explorer", "../resources/fa-free/solid/folder.svg")
        self.actionOpenDirectory.setStatusTip("View File Explorer")
        self.actionOpenDirectory.triggered.connect(self.filesOpenDirectory)   

        self.actionCheckSelected = self._loadActionIcon("&Select", "../resources/fa-free/solid/plus.svg")
        self.actionCheckSelected.setStatusTip("Mark selected for download")
        self.actionCheckSelected.triggered.connect(self.checkSelected)   

        self.actionUncheckSelected = self._loadActionIcon("&Unselect", "../resources/fa-free/solid/minus.svg")
        self.actionUncheckSelected.setStatusTip("Unmark selected for download")
        self.actionUncheckSelected.triggered.connect(self.uncheckSelected)   

        self.tableView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableView.addAction(self.actionViewKitsu)
        self.tableView.addAction(self.actionOpenDirectory)  
        self.tableView.addAction(self.actionCheckSelected)  
        self.tableView.addAction(self.actionUncheckSelected)   

    def checkSelected(self):
        self.checkItems(True)

    def uncheckSelected(self):
        self.checkItems(False)

    def checkItems(self, select):
        idx = self.tableView.selectedIndexes()
        
        for index in idx:
            row_index = index.row()
            try:
                # self.selected_file = self.proxy.data[row_index]  
                self.proxy.setData(self.proxy.index(row_index, PlaylistModel.COL_SELECT), select, QtCore.Qt.EditRole)
            except:
                traceback.print_exc()
                return None                    

    def open_url(self, url):
        link = QtCore.QUrl(url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')              

    def viewInKitsu(self):
        idx = self.tableView.selectedIndexes()
        for index in idx:
            row_index = index.row()
            try:
                self.selected_file = self.proxy.data(self.proxy.index(row_index, 0), QtCore.Qt.UserRole)                
                # self.selected_file = self.proxy.items[row_index]  
                tasks = gazu.task.all_tasks_for_entity_and_task_type(self.selected_file["entity_id"], self.selected_file["task_type_id"])
                if len(tasks) > 0:
                    task = tasks[0]
                    task_url = gazu.task.get_task_url(task)
                    if task_url:
                        self.open_url(task_url)
                        return True

                    
            except:
                traceback.print_exc()
                return None         

    def filesOpenDirectory(self):
        editorial_folder = self.lineEditFolder.text()
        if not (self.tableView.selectedIndexes()):
            return False

        idx = self.tableView.selectedIndexes()
        for index in idx:
            row_index = index.row()
            try:
                # self.selected_file = self.proxy.items[row_index]                
                self.selected_file = self.proxy.data(self.proxy.index(row_index, 0), QtCore.Qt.UserRole)                

                fn, ext = os.path.splitext(self.selected_file["output_file_name"])
                item_name = os.path.normcase("{}_{}_{}".format(self.selected_file["ep"], self.selected_file["sq"], self.selected_file["sh"]))
                output_name = os.path.normcase("{}/{}{}".format(item_name, item_name, ext))

                # D:\Productions\editorial\wotw\wotw_edit\wip\101_ALICKOFPAINT\sc010\sh010\sc010_sh010_Anim-Animation\witw_101_alickofpaint_sc010_sh010_anim_animation_v004.mp4

                file_path = os.path.dirname(os.path.join(editorial_folder, output_name))

                #output_dir = "{}/{}".format(self.lineEditFolder.text(), self.episode["name"])
                #file_path = os.path.normpath(os.path.join(output_dir, self.selected_file["output_file_name"]))

                if os.path.isdir(file_path):
                    #reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    #if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(file_path)
                    return True       

            except:
                traceback.print_exc()
                return None                                  

    def process(self):   
        playlist_filename = self.get_playlist_file_name()

        if os.path.exists(playlist_filename):
            self.load_playlist_file(playlist_filename)
        else:
            self.playlist_file = json.loads("{}")

        old_max = QtCore.QThread.idealThreadCount()
        self.threadpool.setMaxThreadCount(3)
        try:
            model = self.tableView.model()
            
            ## model = self.proxy
            self.count = 0 
            for x in range(model.rowCount()):
                item = model.data(model.index(x, 0), QtCore.Qt.UserRole)
                item_date = datetime.strptime(item["updated_at"], '%Y-%m-%dT%H:%M:%S.%f') #'2022-04-07T11:31:11.419272'
                item["model_index"] = x

                if not item["selected"]:
                    continue

                shot_name = item["shot_name"]

                if not shot_name in self.playlist_file:
                    self.playlist_file[shot_name] = { "version": 1, "updated_at": None }

                playlist_item = self.playlist_file[shot_name]

                should_process = False
                if item["version"] > playlist_item["version"]:
                    should_process = True

                if not playlist_item["updated_at"]:
                    should_process = True
                else:
                    # updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%f')

                    export_date = datetime.strptime(playlist_item["updated_at"], '%Y-%m-%dT%H:%M:%S.%f')

                    if export_date < item_date:
                        should_process = True

                    #item_date = time.str
                    # or playlist_item["updated_at"] < 

                if should_process:
                    print("swing::playlist: processing: {}:{} --> {}".format(item["output_file_name"], item_date, item["shot_name"]))

                    worker = PlaylistWorker(self, item, target = self.lineEditFolder.text(), extract_zips = self.checkBoxExtractZip.isChecked())
                    worker.callback.progress.connect(self.update_progress)
                    worker.callback.done.connect(self.update_done)
                    
                    self.count += 1
                    self.threadpool.start(worker)
                    self.threadpool.waitForDone()

                    self.update()
                    ##worker.run()

                    playlist_item["version"] = item["version"]
                    playlist_item["updated_at"] = item["updated_at"]

                    self.playlist_file[shot_name] = playlist_item                
                else:
                    model.setData(model.index(x, PlaylistModel.COL_STATUS), "Skipped", QtCore.Qt.EditRole)
                    #worker.run()

            self.save_playlist_file(self.get_playlist_file_name())    
            if self.count > 0:        
                self.progressBar.setMaximum(self.count)

            self.validate_folder()

        finally:
            self.threadpool.setMaxThreadCount(old_max)

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

        #if "file_tree" in self.project:
        #    file_tree = self.project['file_tree']
        #    if "editorial" in file_tree:
        #        mount = file_tree["editorial"]["mountpoint"]
        #        mount = mount.replace("/mnt/content/productions", editorial_folder)
        #        editorial_folder = os.path.normpath(os.path.join(mount, file_tree["editorial"]["root"]))

        
        playlist_folder = os.path.normpath(os.path.normcase(os.path.join(editorial_folder, friendly_string(self.project["code"]), friendly_string(self.episode["name"]))))
        self.lineEditFolder.setText(playlist_folder)      

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

    def get_playlist_file_name(self):
        return os.path.join(self.lineEditFolder.text(), PlaylistDialog.PLAYLIST_FILE)

    def select_output_dir(self):
        working_dir = self.lineEditFolder.text()
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Media Directory", working_dir)
        if q:
            self.lineEditFolder.setText(q)

    def load_playlist_file(self, json_file_name):
        with open(json_file_name, 'r') as f:
            self.playlist_file = json.load(f)

    def save_playlist_file(self, json_file_name):
        with open(json_file_name, 'w') as json_file:
            try:
                json.dump(self.playlist_file, json_file, indent=4)        
            except:
                traceback.print_exc(file=sys.stdout)    

    def update_tree(self):
        mode = ""
        if self.radioButtonShowAll.isChecked():
            mode = "all"
        elif self.radioButtonLastDay.isChecked():
            mode = "last_day"
        elif self.radioButtonLatestVersion.isChecked():
            mode = "latest_version"

        self.model = PlaylistModel(self.items, self.task_types, parent = None, mode = mode, sequences = self.checkBoxSequences.isChecked())

        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setFilterKeyColumn(-1) # Search all columns.
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(True)

        self.tableView.setModel(self.proxy)

        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)

        self.tableView.sortByColumn(PlaylistModel.COL_SHOT, QtCore.Qt.AscendingOrder)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.tableView.setColumnWidth(PlaylistModel.COL_SELECT, 40)
        self.tableView.setColumnWidth(PlaylistModel.COL_SHOT, 200)
        self.tableView.setColumnWidth(PlaylistModel.COL_TASK, 120)
        self.tableView.setColumnWidth(PlaylistModel.COL_NAME, 350)
        self.tableView.setColumnWidth(PlaylistModel.COL_VERSION, 40)
        self.tableView.setColumnWidth(PlaylistModel.COL_UPDATED, 160)
        self.tableView.setColumnWidth(PlaylistModel.COL_STATUS, 120)
        self.tableView.setColumnWidth(PlaylistModel.COL_VALIDATION, 200)

        checkboxDelegate = CheckBoxDelegate()
        self.tableView.setItemDelegateForColumn(0, checkboxDelegate)  

        for i in range(self.model.rowCount()):
            self.tableView.resizeRowToContents(i)

        return True
    
    def validate_folder(self):
        target_folder = self.lineEditFolder.text()
        validation_messages = []
        model = self.tableView.model()
        
        ## model = self.proxy
        self.count = 0 
        for x in range(model.rowCount()):
            item = model.data(model.index(x, 0), QtCore.Qt.UserRole)
            item_name = os.path.normcase("{}_{}_{}".format(item["ep"], item["sq"], item["sh"]))

            message = {
                "shot": item_name,
                "exists": True,
                "file_count": 0,
                "dir_count": 0,
                "message": None,
                "invalid_files": 0
            }            
            try:
                #fn, ext = os.path.splitext(item["output_file_name"])
                #output_name = os.path.normcase("{}/{}{}".format(item_name, item_name, ext))  

                shot_directory = os.path.join(target_folder, item_name)          
                if not os.path.exists(shot_directory):
                    message["exists"] = False
                    continue

                file_list = os.listdir(shot_directory)
                if len(file_list) == 0:
                    message["message"] = "No files found"
                    continue
                else:
                    message["file_count"] = len(file_list)

                dir_count = 0
                invalid_files = 0
                for file_name in file_list:
                    test = os.path.join(shot_directory, file_name)

                    if os.path.isdir(test):
                        dir_count += 1

                    fn, ext = os.path.splitext(test)    

                    if any(ext in invalid for invalid in PlaylistDialog.INVALID_FILE_TYPES):  
                        invalid_files += 1

                message["dir_count"] = dir_count
                message["invalid_files"] = invalid_files                
                # check for 
            finally:
                validation_result = ""
                if message["invalid_files"] > 0:
                    validation_result += "Error: Invalid files found"

                if message["dir_count"] > 0:
                    if len(validation_result) > 0:
                        validation_result += ", "
                    validation_result += "Error: Sub directories found"

                message["message"] = validation_result
                validation_messages.append(message)     

                if len(validation_result) > 0:
                    item = model.setData(model.index(x, PlaylistModel.COL_VALIDATION), validation_result, QtCore.Qt.EditRole)                    


class PlaylistModel(QtCore.QAbstractTableModel):

    COLUMNS = ["", "Shot", "Task", "v", "Frames", "In", "Out", "File Name", "Updated", "Status", "Messages" ]
    items = []

    COL_SELECT = 0
    COL_SHOT = 1
    COL_TASK = 2        
    COL_VERSION = 3    

    COL_FRAMES = 4
    COL_IN = 5
    COL_OUT = 6

    COL_NAME = 7
    COL_UPDATED = 8
    COL_STATUS = 9

    COL_VALIDATION = 10

    def __init__(self, data, task_types, parent = None, mode = "show_all", sequences = False):
        super(PlaylistModel, self).__init__(parent)

        self.task_type_dict = {}
        self.sequences = sequences
        self.ignore_zips = True

        for item in task_types:
            self.task_type_dict[item["name"]] = item
            if "render" in item["name"].lower():
                self.ignore_zips = False

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

            ## ignore 'FOR MGFX' in file:
            if "for mgfx" in item["output_file_name"].lower():
                print("swing::playlists skipping {}".format(item["output_file_name"]))
                continue                

            ## if viewing sequences
            if self.sequences:
                # only show shot 00's
                if not item["sh"].lower() == "sh000":
                    continue

            else:
                # otherwise always skip shot 00's
                if item["sh"].lower() == "sh000":
                    continue

            if self.ignore_zips:
                if ".zip" in item["output_file_name"].lower() or ".7z" in item["output_file_name"].lower():
                    continue

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
                    shots = sorted(shots, key = lambda x: x["updated_at"], reverse=True)

                    revision = len(shots)

                    for sh in shots:
                        sh["shot_name"] = shot_name
                        sh["selected"] = True
                        sh["status"] = ""
                        sh["message"] = None
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
                
            elif col_index == PlaylistModel.COL_VALIDATION:
                if item["message"] and len(item["message"]) > 0:
                    message = item["message"]
                    if "error" in message.lower():
                        return QtGui.QColor.red
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

        elif PlaylistModel.COL_FRAMES == col_index:
            return item["nb_frames"]

        elif PlaylistModel.COL_IN == col_index:
            if item["data"] and "frame_in" in item["data"]:
                return item["data"]["frame_in"]

        elif PlaylistModel.COL_OUT == col_index:
            if item["data"] and "frame_out" in item["data"]:
                return item["data"]["frame_out"]                                    

        elif PlaylistModel.COL_VERSION == col_index:
            return item["version"]            

        elif PlaylistModel.COL_NAME == col_index:
            return item["output_file_name"]

        elif PlaylistModel.COL_UPDATED == col_index:
            return item["updated_at"]

        elif PlaylistModel.COL_STATUS == col_index:
            return item["status"]
        
        elif PlaylistModel.COL_VALIDATION == col_index:
            return item["message"]

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

        elif PlaylistModel.COL_VALIDATION == col_index:
            item["message"] = str(value)
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
    playlist_dialog = PlaylistDialog(None)

    settings = SwingSettings.get_instance()
    connect_to_server(settings.swing_user(), settings.swing_password())

    project = gazu.project.get_project_by_name("Tom Gates S3")
    episode = gazu.shot.get_episode_by_name(project, "tg_2d_ep301")
    task_type = gazu.task.get_task_type_by_name('Anim-Final')

    playlist_dialog.set_project_episode(project["id"], episode["id"], [ task_type ])
   
    playlist_dialog.show()
    playlist_dialog.validate_folder()    
    sys.exit(app.exec_())