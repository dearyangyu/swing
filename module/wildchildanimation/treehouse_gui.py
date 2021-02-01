# -*- coding: utf-8 -*-
import traceback
import sys

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

import os
import keyring
import gazu
import traceback
import os.path

import requests
import background_workers as bg

from gui.main_form import Ui_WcaMayaDialog
from gui.connection_dialog import Ui_ConnectionDialog
from gui.publish_dialog import Ui_PublishDialog
from gui.download_dialog import Ui_DownloadDialog

# DOWNLOAD_SERVER = "http://production.wildchildanimation.com/edit"
DOWNLOAD_SERVER = "http://10.147.19.55:8202/edit"

def resource_path(resource):
    base_path = os.path.dirname(os.path.realpath(__file__))
    #uic.loadUi(os.path.join(root, resource_file), self)
    #base_path = os.path.abspath(".")
    return os.path.join(base_path, resource)


class TreehouseGUI(QtWidgets.QDialog, Ui_WcaMayaDialog):
    user_email = None
    tasks = []

    currentProject = None
    currentEpisode = None
    currentSequence = None
    currentShot = None
    currentTask = None
    currentAssetType = None
    currentAsset = None
    gazu_client = None
    connected = False

    def __init__(self, parent = None):
        super(TreehouseGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.comboBoxSequence.currentIndexChanged.connect(self.sequence_changed)

        self.comboBoxAssetType.currentIndexChanged.connect(self.asset_type_changed)
        
        self.comboBoxAsset.currentIndexChanged.connect(self.load_asset_files)
        self.comboBoxShot.currentIndexChanged.connect(self.load_shot_files)    

        self.pushButtonSettings.clicked.connect(self.open_connection_settings)
        self.pushButtonConnect.clicked.connect(self.connect_to_server)
        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonPublish.clicked.connect(self.publish_scene)

        if self.connect_to_server():
            self.refresh_data()


    def open_connection_settings(self):
        dialog = ConnectionDialogGUI(self)

        dialog.lineEditServer.setText(load_settings('studiocontrol', 'server', 'https://production.wildchildanimation.com'))
        dialog.lineEditEmail.setText(load_settings('studiocontrol', 'user', 'user@example.com'))
        dialog.lineEditPassword.setText(load_settings('studiocontrol', 'password', 'Not A Password'))

        dialog.exec_()
        print("loading settings")


    def connect_to_server(self): 
        if self.connected and self.gazu_client:
            self.gazu_client = None
            self.connected = False

        server = load_settings('studiocontrol', 'server', 'https://production.wildchildanimation.com')
        email = load_settings('studiocontrol', 'user', 'user@example.com')
        password = load_settings('studiocontrol', 'password', 'Not A Password')

        gazu.set_host(server)
        try:
            self.gazu_client = gazu.log_in(email, password)
            self.connected = True
            self.user_email = email
            self.pushButtonConnect.setText("Reconnect")

            self.refresh_data()
        except:
            return False

        return True

    def refresh_data(self):
        print("[refresh_data]")
        loader = bg.ProjectLoaderThread(self)
        loader.loaded.connect(self.projects_loaded)
        loader.start()

    def clear_combo(self, combo):
        combo.blockSignals(True)
        combo.clear()
        combo.blockSignals(False)

    def projects_loaded(self, data): 
        print("[projects_loaded]")

        self.projects = data

        self.clear_combo(self.comboBoxProject)
        self.clear_combo(self.comboBoxEpisode)
        self.clear_combo(self.comboBoxSequence)
        self.clear_combo(self.comboBoxShot)
        self.clear_combo(self.comboBoxAssetType)

        if len(self.projects) == 0:
            return False

        self.comboBoxProject.blockSignals(True)
        for p in self.projects:
            self.comboBoxProject.addItem(p["name"])            

        self.comboBoxProject.blockSignals(False)
        
    def project_changed(self, index):
        print("[project_changed]")

        self.currentProject = self.projects[index]
        self.currentProjectIndex = index

        self.clear_combo(self.comboBoxEpisode)
        self.clear_combo(self.comboBoxSequence)
        self.clear_combo(self.comboBoxShot)
        self.clear_combo(self.comboBoxAssetType)

        ep_loader = bg.EpisodeLoaderThread(self, self.currentProject)
        ep_loader.loaded.connect(self.episode_loaded)
        ep_loader.start()

        asset_loader = bg.AssetTypeLoaderThread(self, self.currentProject)
        asset_loader.loaded.connect(self.asset_types_loaded)
        asset_loader.start()

        task_loader = bg.TaskLoaderThread(self, self.currentProject, self.user_email)
        task_loader.loaded.connect(self.tasks_loaded)
        task_loader.start()


    def episode_loaded(self, data): 
        print("[episode_loaded]")
        self.episodes = data

        self.clear_combo(self.comboBoxSequence)
        self.clear_combo(self.comboBoxShot)
        self.clear_combo(self.comboBoxEpisode)

        last = self.comboBoxEpisode.currentIndex()
        for p in self.episodes:
            self.comboBoxEpisode.addItem(p["name"])            

        if last == -1 and len(data) > 0:
            last = 0
        
        self.comboBoxEpisode.setCurrentIndex(last)

    def asset_types_loaded(self, data): 
        print("[asset_types_loaded]")
        self.asset_types = data

        self.clear_combo(self.comboBoxAssetType)

        last = self.comboBoxAssetType.currentIndex()
        for p in self.asset_types:
            name = "{} {}".format(self.currentProject["code"], p["name"])            
            self.comboBoxAssetType.addItem(name)            

        if last == -1 and len(data) > 0:
            last = 0
        
        self.comboBoxAssetType.setCurrentIndex(last)    

    def tasks_loaded(self, data):
        print("[tasks_loaded]")

        self.tasks = data
        self.load_task_list_widget(self.tasks)

    def episode_changed(self, index):
        print("[episode_changed]")
        self.currentEpisode = self.episodes[index]
        self.currentEpisodeIndex = index

        loader = bg.SequenceLoaderThread(self, self.currentProject, self.currentEpisode)
        loader.loaded.connect(self.sequence_loaded)
        loader.start() 

    def sequence_loaded(self, data): 
        print("[sequence_loaded]")
        self.sequences = data

        self.clear_combo(self.comboBoxSequence)
        self.clear_combo(self.comboBoxShot)

        if len(self.sequences) == 0:
            return False

        last = self.comboBoxSequence.currentIndex()
        for p in self.sequences:
            name = "{} {} {}".format(self.currentProject["code"], self.currentEpisode["name"],  p["name"])
            self.comboBoxSequence.addItem(name)            

        if last == -1 and len(data) > 0:
            last = 0
        
        self.comboBoxSequence.setCurrentIndex(last)

    def sequence_changed(self, index):
        print("[sequence_changed]")

        self.currentSequence = self.sequences[index]
        self.currentSequenceIndex = index

        loader = bg.ShotLoaderThread(self, self.currentProject, self.currentSequence)
        loader.loaded.connect(self.shot_loaded)
        loader.start() 

    def asset_type_changed(self, index):
        print("[asset_type_changed]")
        self.currentAssetType = self.asset_types[index]

        loader = bg.AssetLoaderThread(self, self.currentProject, self.currentAssetType)
        loader.loaded.connect(self.asset_loaded)
        loader.start()

    def shot_loaded(self, data): 
        print("[shot_loaded]")

        self.shots = data

        self.clear_combo(self.comboBoxShot)

        last = self.comboBoxShot.currentIndex()
        for p in self.shots:
            name = "{} {} {} {}".format(self.currentProject["code"], self.currentEpisode["name"], self.currentSequence["name"], p["name"])
            self.comboBoxShot.addItem(name)            
        
        self.comboBoxShot.setCurrentIndex(last)

    def load_shot_files(self, index):
        self.currentShot = self.shots[index]

        print("load shot files {}".format(index))

        output_files = gazu.files.all_output_files_for_entity(self.currentShot)
        working_files = gazu.files.get_all_working_files_for_entity(self.currentShot)

        self.load_file_tree_widget(output_files, working_files)        
        print("Loaded {} output files, {} working files".format(len(output_files), len(working_files)))

    def asset_loaded(self, data): 
        print("[asset_loaded]")

        self.assets = data
        self.clear_combo(self.comboBoxAsset)

        last = self.comboBoxAsset.currentIndex()
        for p in self.assets:
            name = "{} {} {} {}".format(self.currentProject["code"], self.currentEpisode["name"], self.currentSequence["name"], p["name"])
            self.comboBoxAsset.addItem(name)            
        
        self.comboBoxAsset.setCurrentIndex(last)

    def load_asset_files(self, index):
        self.currentAsset = self.assets[index]

        print("load asset files {}".format(index))

        output_files = gazu.files.all_output_files_for_entity(self.currentAsset)
        working_files = gazu.files.get_all_working_files_for_entity(self.currentAsset)

        self.load_file_tree_widget(output_files, working_files)
        print("Loaded {} output files, {} working files".format(len(output_files), len(working_files)))        

    def load_file_tree_widget(self, output_files = None, working_files = None):
        self.treeWidgetFiles.clear()

        root = QtWidgets.QTreeWidgetItem(["Files"])
        if output_files:
            for item in output_files:
                ti = QtWidgets.QTreeWidgetItem(['{}'.format(item["name"])])
                ti.setCheckState(0, QtCore.Qt.Checked)
                ti.setData(0, QtCore.Qt.UserRole, { "file": item } )
                root.addChild(ti)
            
        if working_files:
            for item in working_files:
                ti = QtWidgets.QTreeWidgetItem(['{}'.format(item["name"])])
                ti.setCheckState(0, QtCore.Qt.Checked)                
                ti.setData(0, QtCore.Qt.UserRole, { "file": item } )
                root.addChild(ti)      

        self.treeWidgetFiles.addTopLevelItem(root)   
        self.treeWidgetFiles.expandAll()       

    def load_task_list_widget(self, tasks = None):
        self.listWidgetTasks.clear()

        for item in tasks:
            name = '{}'.format(item["project_name"])
            name = '{} {}'.format(name, item["entity_type_name"])
            name = '{} {}'.format(name, item["entity_name"])
            name = '{} {}'.format(name, item["task_type_name"])

            li = QtWidgets.QListWidgetItem(name)
            li.setData(QtCore.Qt.UserRole, { "task": item } )

            self.listWidgetTasks.addItem(li)
        self.pushButtonPublish.setEnabled(len(tasks) > 0)


    def download_files(self):
        file_list = []
        for item in self.treeWidgetFiles.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
            if (item.childCount() == 0 and item.checkState(0) > 0):
                file_list.append(item.data(0, QtCore.Qt.UserRole))
        print("Downloading {} files".format(len(file_list)))

        dialog = DownloadDialogGUI(self)
        dialog.resize(self.size())
        dialog.load_files(file_list)
        dialog.exec_()

    def publish_scene(self):
        dialog = PublishDialogGUI(self, self.listWidgetTasks.currentItem().data(QtCore.Qt.UserRole))
        dialog.resize(self.size())
        dialog.exec_()

class ConnectionDialogGUI(QtWidgets.QDialog, Ui_ConnectionDialog):

    def __init__(self, parent = None):
        super(ConnectionDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)

        #resource_file = "gui/forms/maya/connection_dialog.ui"
        #uic.loadUi(resource_path(resource_file), self)

        self.buttonBox.accepted.connect(self.save_settings)

    def save_settings(self):
        self.buttonBox.accepted.disconnect()

        keyring.set_password('studiocontrol', 'server', self.lineEditServer.text())
        keyring.set_password('studiocontrol', 'user', self.lineEditEmail.text())
        keyring.set_password('studiocontrol', 'password', self.lineEditPassword.text())

        self.buttonBox.accepted.connect(self.save_settings)
        return True

class PublishDialogGUI(QtWidgets.QDialog, Ui_PublishDialog):

    def __init__(self, parent = None, item = None):
        super(PublishDialogGUI, self).__init__() # Call the inherited classes __init__ method
        self.setupUi(self)

        self.task = item["task"]
        self.last_dir = None

        #resource_file = "gui/forms/maya/publish_dialog.ui"
        #uic.loadUi(resource_path(resource_file), self)

        name = '{}'.format(self.task["project_name"])
        name = '{} {}'.format(name, self.task["entity_type_name"])
        name = '{} {}'.format(name, self.task["entity_name"])
        name = '{} {}'.format(name, self.task["task_type_name"])        

        self.lineEditTask.setText(name)

        self.projectFileToolButton.clicked.connect(self.select_project_file)
        self.fbxFileToolButton.clicked.connect(self.select_fbx_file)
        self.reviewFileToolButton.clicked.connect(self.select_review_file)

        self.pushButtonOK.clicked.connect(self.accept)
        self.pushButtonCancel.clicked.connect(self.close_dialog)        

    def close_dialog(self):
        self.close()

    def get_references(self):
        return []

    def select_project_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."
        
        #Get the file location
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Open Project File", self.last_dir, "C4d (*.c4d), All Files (*.*)")
        if (file):
            self.projectFileEdit.setText(file[0])
            self.last_dir = file[0]

    def select_fbx_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."

        
        #Get the file location
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Open Output File", self.last_dir, "FBX (*.fbx), All Files (*.*)")
        if (file):
            self.fbxFileEdit.setText(file[0])
            self.last_dir = file[0]

    def select_review_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."

        
        #Get the file location
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Open Review File", self.last_dir, "Images (*.bmp, *.jpg, *.png), Videos (*.mp4), All Files (*.*)")
        if (file):
            self.reviewFileEdit.setText(file[0])
            self.reviewTitleLineEdit.setText(file[0])
            self.last_dir = file[0]


class DownloadDialogGUI(QtWidgets.QDialog, Ui_DownloadDialog):

    working_dir = None
    
    def __init__(self, parent = None):
        super(DownloadDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)

        self.pushButtonSelectWorkingDir.clicked.connect(self.select_wcd)
        self.pushButtonDownload.clicked.connect(self.download_files)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

    def close_dialog(self):
        self.close()

    def select_wcd(self):
        self.working_dir  = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        self.lineEditWorkingDirectory.setText(self.working_dir)

    def load_files(self, files):
        self.files = files

        #Row count 
        self.tableWidget.setRowCount(len(self.files))
  
        #Column count 
        self.tableWidget.setColumnCount(5)
        row = 0
        for item in self.files:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item["file"]["name"])) 
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item["file"]["revision"])) 
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item["file"]["updated_at"])) 
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("0") )
            row = row + 1

        self.tableWidget.setHorizontalHeaderLabels([
            'Name', 'Revision', 'Last Updated', '', ''
        ]
        )
   
        #Table will fit the screen horizontally 
        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.tableWidget.horizontalHeader().setSectionResizeMode( QtWidgets.QHeaderView.Stretch) 

    def download_files(self):
        self.pushButtonDownload.blockSignals(True)

        email = load_settings('studiocontrol', 'user', 'user@example.com')
        password = load_settings('studiocontrol', 'password', 'Not A Password')

        row = 0
        for file_item in self.files:
            item = file_item["file"]
            #self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item["file"]["name"])) 
            #self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item["file"]["revision"])) 
            #self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item["file"]["updated_at"])) 
            print("Downloading {} to {}".format(item["name"], self.working_dir))

            if "working_file" in item["type"]:
                #working_file = gazu.files.get_working_file(item["id"])
                #gazu.files.download_working_file(item['id'], self.working_dir)

                #source = os.path.join(output_file["path"], output_file["name"])
                target = os.path.join(self.working_dir, item["name"])

                url = "{}/api/working_file/{}".format(DOWNLOAD_SERVER, item["id"])
                #wget.download(url, target,  self.tableWidget.getItem(row, 3))
                rq = requests.get(url, auth=(email, password))
                if rq.status_code == 200:
                    with open(target, 'wb') as out:
                        for bits in rq.iter_content():
                            out.write(bits)

                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("Done") )
            else:
                # output_file = gazu.files.get_output_file(item["id"])

                #source = os.path.join(output_file["path"], output_file["name"])
                target = os.path.join(self.working_dir, item["name"])

                url = "{}/api/output_file/{}".format(DOWNLOAD_SERVER, item["id"])
                params = { 
                    "username": email,
                    "password": password
                }
                #wget.download(url, target)

                rq = requests.post(url, data = params)
                if rq.status_code == 200:
                    with open(target, 'wb') as out:
                        for bits in rq.iter_content():
                            out.write(bits)

                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("Done") )

            row = row + 1        

        self.pushButtonDownload.blockSignals(False)

     

def load_settings(key, val, default):
    result = keyring.get_password(key, val)
    if result == None:
        keyring.set_password(key, val, default)
        result = keyring.get_password(key, val)
    return result
