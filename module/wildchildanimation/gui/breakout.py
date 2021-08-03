# -*- coding: utf-8 -*-

import traceback
import sys
import os
import json

from wildchildanimation.gui.settings import SwingSettings

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
from wildchildanimation.gui.breakout_upload_dialog import Ui_BreakoutUploadDialog
from wildchildanimation.gui.swing_tables import human_size, load_file_table_widget

from wildchildanimation.gui.background_workers import ShotCreator, ShotCreatorSignal

from wildchildanimation.gui.media_info import *


'''
    BreakoutUploadDialog class
    ################################################################################
'''

class BreakoutUploadDialog(QtWidgets.QDialog, Ui_BreakoutUploadDialog):

    working_dir = None
    
    def __init__(self, parent = None):
        super(BreakoutUploadDialog, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint ^ QtCore.Qt.WindowMinMaxButtonsHint)

        set_button_icon(self.toolButtonSelectPlayblasts, "../resources/fa-free/solid/info-circle.svg")
        set_button_icon(self.toolButtonSelectProjects, "../resources/fa-free/solid/info-circle.svg")        

        self.pushButtonCancel.clicked.connect(self.close_dialog)

        self.pushButtonScan.clicked.connect(self.scan)
        self.pushButtonCreate.clicked.connect(self.process)

        self.pushButtonLoad.clicked.connect(self.load)
        self.pushButtonSave.clicked.connect(self.save)

        self.toolButtonSelectPlayblasts.clicked.connect(self.select_playblast_folder)
        self.toolButtonSelectProjects.clicked.connect(self.select_project_files_folder)

        self.model = None
        self.project = None
        self.episode = None
        self.sequences = None
        self.shot_list = {}
        self.swing_settings = SwingSettings.get_instance()

        self.lineEditPlayblastFolder.setText(load_settings("last_breakout_playblast", os.path.expanduser("~")))
        self.lineEditProjectsFolder.setText(load_settings("last_breakout_projects", os.path.expanduser("~")))

        self.ffprobe_bin = self.swing_settings.bin_ffprobe()
        self.pushButtonFfprobe.setEnabled(self.ffprobe_bin is not None)
        self.pushButtonFfprobe.clicked.connect(self.ffprobe)
        self.pushButtonSetRange.clicked.connect(self.set_range)

        self.threadpool = QtCore.QThreadPool.globalInstance()
        

    def save(self):
        #Get the file location
        q = QtWidgets.QFileDialog.getSaveFileName(self, "select json file", load_settings("last_breakout", os.path.expanduser("~")), "All Files (*.*)")
        if not (q):
            return 

        self.model.save_to_file(q[0])
        save_settings("last_breakout", q[0])        

    def load(self):
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(self, "select json file", load_settings("last_breakout", os.path.expanduser("~")), "All Files (*.*)")
        if not (q):
            return 

        if not self.model:
            self.model = ShotlistModel(self)
        
        self.model.load_from_file(q[0])
        self.tableView.setModel(self.model)

        save_settings("last_breakout", q[0]) 

    def close_dialog(self):
        self.close()        

    def select_playblast_folder(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select playblast directory')
        if (dir):
            save_settings("last_breakout_playblast", dir)

            self.lineEditPlayblastFolder.setText(dir)
            self.check_files()

    def select_project_files_folder(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select project files directory')
        if (dir):
            save_settings("last_breakout_projects", dir)

            self.lineEditProjectsFolder.setText(dir)            
            self.check_files()

    def check_files(self):
        project_dir = self.lineEditProjectsFolder.text()
        if os.path.exists(project_dir):
            print("scanning project files")

        playblast_dir = self.lineEditPlayblastFolder.text()
        if os.path.exists(project_dir):
            print("scanning playblast files")

    def process(self):    
        project = self.project
        episode = self.episode

        if self.checkBoxSequence.isChecked():
            sequence = self.episode["sequences"][self.comboBoxSequence.currentIndex()]
            shot_list = self.model.shots

            self.threadpool = QtCore.QThreadPool.globalInstance()        

            worker = ShotCreator(self, self.project, self.episode, sequence, shot_list)
            worker.callback.results.connect(self.results)

            #self.threadpool.start(worker)
            worker.run()
        else:
            QtWidgets.QMessageBox.info(self, 'Break Out', 'Please select a sequence')               
            #worker.run()

    def results(self, results):        
        self.lineEdit.setText(results["message"])

    def ffprobe(self):
        for item in self.model.shots:
            if "playblast_file_path" in item and item["playblast_file_path"]:
                worker = MediaInfo(self, self.ffprobe_bin, item["playblast_file_path"], item)
                worker.callback.info.connect(self.media_info)
                self.threadpool.start(worker)

    def set_range(self):
        start_frame = self.spinBoxStartingFrame.value()
        handles = self.checkBoxHandles.isChecked()
        handle_count = self.spinBoxHandles.value()

        for item in self.model.shots:
            if item["nb_frames"]:
                nb_frames = int(item["nb_frames"])

                item["in"] = str(start_frame)
                start_frame += nb_frames

                if handles:
                    start_frame += handle_count
                    
                item["out"] = str(start_frame)
                start_frame += 1                

        self.model.layoutChanged.emit()
                

    def media_info(self, results):
        item = results["item"]
        item["nb_frames"] = results["results"]

        self.model.layoutChanged.emit()

    def scan(self):
        save_settings("last_breakout_playblast", self.lineEditPlayblastFolder.text())
        save_settings("last_breakout_projects", self.lineEditProjectsFolder.text())

        # scan for playblasts
        root_folder = self.lineEditPlayblastFolder.text()
        if len(root_folder.strip()) > 0:
            for item in os.listdir(root_folder):
                if ".mov" in item or ".mp4" in item:
                    shot_number = os.path.splitext(item)[0].split("_")[2]
                    if not shot_number in self.shot_list:
                        shot = {
                            "shot_number": shot_number.strip(),
                            "in": None, "out" : None, "nb_frames": None, "status": None,
                            "playblast_file_name": item,
                            "playblast_file_path": os.path.normpath(os.path.join(root_folder, item))
                        }
                    else:
                        shot = self.shot_list[shot_number]
                        shot["playblast_file_name"] = item,
                        shot["playblast_file_path"] = os.path.normpath(os.path.join(root_folder, item))

                    self.shot_list[shot_number] = shot

        # scan for project files
        root_folder = self.lineEditProjectsFolder.text()
        if len(root_folder.strip()) > 0:        
            for item in os.listdir(root_folder):
                if ".ma" in item or ".mb" in item and item not in [ ".mayaSwatches"]:
                    try:
                        shot_number = os.path.splitext(item)[0].split("_")[2]
                        if not shot_number in self.shot_list:
                            shot = {
                                "shot_number": shot_number.strip(),
                                "in": None, "out" : None, "nb_frames": None, "status": None,
                                "project_file_name": item,                        
                                "project_file_path": os.path.normpath(os.path.join(root_folder, item))
                            }
                        else:
                            shot = self.shot_list[shot_number]
                            shot["project_file_name"] = item
                            shot["project_file_path"] = os.path.normpath(os.path.join(root_folder, item))

                        self.shot_list[shot_number] = shot
                    except:
                        print("skipping {}".format(item[0]))

        self.model = ShotlistModel(self, self.shot_list)
        self.tableView.setModel(self.model)

        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectItems)
        self.tableView.setColumnWidth(0, 100)
        self.tableView.setColumnWidth(1, 200)
        self.tableView.setColumnWidth(2, 200)
        self.tableView.setColumnWidth(3, 75)
        self.tableView.setColumnWidth(4, 75)

        self.tableView.verticalHeader().setDefaultSectionSize(self.tableView.verticalHeader().minimumSectionSize())

    def set_project(self, project):
        self.project = project

    def set_episode(self, episode):
        self.episode = episode
        #self.sequences = self.episode["sequences"]

    def set_sequence(self, sequence):
        self.comboBoxSequence.setCurrentIndex(self.comboBoxSequence.findData(sequence))

class ShotlistModel(QtCore.QAbstractTableModel):

    columns = [
        "Shot", "Playblast", "Project", "Frames", "In", "Out", "Status"
    ]    

    def __init__(self, parent, shots = None):
        super(ShotlistModel, self).__init__(parent)
        self.shots = []
        if shots:
            for item in shots:
                shot = shots[item]
                self.shots.append(shot)

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            item = self.shots[index.row()]
            col = index.column()

            if 0 == col:
                item["shot_number"] = "{}".format(value)
                return True
            elif 3 == col:
                item["nb_frames"] = str(value)
                return True
            elif 4 == col:
                item["in"] = str(value)
                return True
            elif 5 == col:
                item["out"] = str(value)
                return True

            return False

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
            item = self.shots[index.row()]

            col = index.column()
            if 0 == col:
                return item["shot_number"]
            elif 1 == col:
                if "playblast_file_name" in item:
                    return item["playblast_file_name"]
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
        return len(self.shots)   

    def load_from_file(self, json_file_name):
        with open(json_file_name, 'r') as f:
            self.shots = json.load(f)
        self.layoutChanged.emit()

    def save_to_file(self, json_file_name):
        with open(json_file_name, 'w') as json_file:
            json.dump(self.shots, json_file)