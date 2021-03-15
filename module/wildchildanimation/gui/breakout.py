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

from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.breakout_upload_dialog import Ui_BreakoutUploadDialog
from wildchildanimation.gui.swing_tables import human_size, load_file_table_widget

from wildchildanimation.background_workers import ShotCreator, ShotCreatorSignal

'''
    BreakoutUploadDialog class
    ################################################################################
'''

class BreakoutUploadDialog(QtWidgets.QDialog, Ui_BreakoutUploadDialog):

    working_dir = None
    
    def __init__(self, parent = None):
        super(BreakoutUploadDialog, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.toolButtonSelectPlayblasts.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonSelectProjects.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))

        self.pushButtonCancel.clicked.connect(self.close_dialog)

        self.pushButtonScan.clicked.connect(self.scan)
        self.pushButtonCreate.clicked.connect(self.process)

        self.toolButtonSelectPlayblasts.clicked.connect(self.select_playblast_folder)
        self.toolButtonSelectProjects.clicked.connect(self.select_project_files_folder)

        self.project = None
        self.episode = None
        self.sequences = None
        self.shot_list = {}

        self.lineEditPlayblastFolder.setText(load_settings("last_breakout_playblast", os.path.expanduser("~")))
        self.lineEditProjectsFolder.setText(load_settings("last_breakout_projects", os.path.expanduser("~")))

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
        sequence = self.episode["sequences"][self.comboBoxSequence.currentIndex()]
        shot_list = self.model.shots

        self.threadpool = QtCore.QThreadPool.globalInstance()        

        worker = ShotCreator(self, project, episode, sequence, shot_list)
        worker.callback.results.connect(self.results)

        self.threadpool.start(worker)
        #worker.run()

    def results(self, results):        
        self.lineEdit.setText(results["message"])

    def scan(self):
        save_settings("last_breakout_playblast", self.lineEditPlayblastFolder.text())
        save_settings("last_breakout_projects", self.lineEditProjectsFolder.text())

        # scan for playblasts
        root_folder = self.lineEditPlayblastFolder.text()
        for item in os.listdir(root_folder):
            if ".mov" in item or ".mp4" in item:
                shot_number = os.path.splitext(item)[0].split("_")[1]
                if not shot_number in self.shot_list:
                    shot = {
                        "shot_number": shot_number,
                        "in": None, "out" : None, "status": None,
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
        for item in os.listdir(root_folder):
            if ".ma" in item or ".mb" in item:
                shot_number = os.path.splitext(item)[0].split("_")[1]
                if not shot_number in self.shot_list:
                    shot = {
                        "shot_number": shot_number,
                        "in": None, "out" : None, "status": None,                        
                        "project_file_name": item,                        
                        "project_file_path": os.path.normpath(os.path.join(root_folder, item))
                    }
                else:
                    shot = self.shot_list[shot_number]
                    shot["project_file_name"] = item
                    shot["project_file_path"] = os.path.normpath(os.path.join(root_folder, item))

                self.shot_list[shot_number] = shot

        self.model = ShotlistModel(self, self.shot_list)
        self.tableView.setModel(self.model)

        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectItems)
        self.tableView.setColumnWidth(0, 100)
        self.tableView.setColumnWidth(1, 200)
        self.tableView.setColumnWidth(2, 200)
        self.tableView.setColumnWidth(3, 75)
        self.tableView.setColumnWidth(4, 75)

    def set_project(self, project):
        self.project = project
        self.lineEditProject.setText(self.project["name"])

    def set_episode(self, episode):
        self.episode = episode
        self.lineEditEpisode.setText(self.episode["name"])
        self.sequences = self.episode["sequences"]
        self.comboBoxSequence.clear()

        for item in self.sequences:
            self.comboBoxSequence.addItem(item["name"])

class ShotlistModel(QtCore.QAbstractTableModel):

    #columns = [
    #    "Shot", "Playblast", "Project", "In", "Out", "Status"
    #]    

    columns = [
        "Shot", "Playblast", "Project"
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
                item["in"] = str(value)
                return True
            elif 4 == col:
                item["out"] = str(value)
                return True

            return False

    def flags(self, index):
        col = index.column()
        if col in [0, 3, 4]:
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
                return item["in"]
            elif 4 == col:
                return item["out"]
            elif 5 == col:
                return item["status"]

    def rowCount(self, index):
        return len(self.shots)   

