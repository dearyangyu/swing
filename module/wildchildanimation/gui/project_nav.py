# -*- coding: utf-8 -*-

import traceback
import sys
import os
import copy

# ==== auto Qt load ====
try:
    from PySide2.QtWidgets import QApplication, QWidget, QStyle
    from PySide2.QtCore import Signal as pyqtSignal
    from PySide2.QtCore import QObject, QThreadPool
    from PySide2 import QtGui
    qtMode = 0
except ImportError:
    from PyQt5.QtWidgets import QApplication, QWidget, QStyle
    from PyQt5.QtCore import pyqtSignal
    from PyQt5.QtCore import QObject, QThreadPool
    from PyQt5 import QtGui
    qtMode = 1

# === theme it dark
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False

from wildchildanimation.gui.swing_utils import connect_to_server, write_log, load_keyring, load_settings, save_settings, set_button_icon
from wildchildanimation.gui.background_workers import ProjectLoaderThread, ProjectHierarchyLoaderThread
from wildchildanimation.gui.project_nav_widget import Ui_ProjectNavWidget
from wildchildanimation.gui.entity_select import *

import wildchildanimation.gui.resources.swing_resources

class NavigationChangedSignal(QObject):

    # setting up custom signal
    selection_changed = pyqtSignal(str, object) 

class ProjectNavWidget(QWidget, Ui_ProjectNavWidget):

    _projects = []
    _episodes = []
    _sequences = []

    _task_types = []
    _user_task_types = []

    _task_status = []
    _user_task_status = []

    _status = { 
        "projects": False,
        "episodes": False,
        "sequences": False
    }
    
    def __init__(self):
        super(ProjectNavWidget, self).__init__(None) # Call the inherited classes __init__ method
        self.threadpool = QThreadPool.globalInstance()

        self.setupUi(self)
        self.readSettings()

        self.toolButtonRefresh.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))

        self.toolButtonRefresh.clicked.connect(self.load_project_hierarchy)

        self.toolButtonTaskTypes.clicked.connect(self.select_task_types)
        set_button_icon(self.toolButtonTaskTypes, ":/swing/gui/fontawesome/solid/lines")

        self.toolButtonStatusTypes.clicked.connect(self.select_status_types)
        set_button_icon(self.toolButtonStatusTypes, ":/swing/gui/fontawesome/solid/task")        

        self.signal = NavigationChangedSignal()
        self.signal.selection_changed.connect(self.selection_changed)

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.comboBoxSequence.currentIndexChanged.connect(self.sequence_changed)


    # load main dialog state
    def readSettings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("ProjectNav")
        self._user_task_types = self.settings.value("task_types", [])
        self._user_task_status = self.settings.value("status_codes", [])
        self.settings.endGroup()            

        #self.settings.beginGroup("Selection")
        #self.last_project = self.settings.value("last_project")
        #self.last_sequences = self.settings.value("last_project")
        #self.last_shot = self.settings.value("last_project")
        #self.settings.endGroup()          


    def select_task_types(self):
        dialog = EntitySelectDialog(self, "Select Task Types")
        dialog.load(self._task_types, self._user_task_types)
        if dialog.exec_():
            self._user_task_types = dialog.get_selection()
            self.task_types_changed(self._user_task_types)

            if len(self._user_task_types) > 0 and len(self._user_task_types) != len(self._task_types):
                self.toolButtonTaskTypes.setStyleSheet("background-color: #505569;")            
            else:
                self.toolButtonTaskTypes.setStyleSheet(None)

    def select_status_types(self):
        dialog = EntitySelectDialog(self, "Select Status Codes")
        dialog.load(self._task_status, self._user_task_status)
        if dialog.exec_():
            self._user_task_status = dialog.get_selection()
            self.status_codes_changed(self._user_task_status)

            if len(self._user_task_status) > 0 and len(self._user_task_status) != len(self._task_status):
                self.toolButtonStatusTypes.setStyleSheet("background-color: #505569;")            
            else:
                self.toolButtonStatusTypes.setStyleSheet(None)

    def is_loaded(self):
        return self._status["projects"] and self._status["episodes"] and self._status["sequences"]

    def get_project(self):
        if self.comboBoxProject.currentIndex() >= 0:
            return self._projects[self.comboBoxProject.currentIndex()]
        return None

    def get_episode(self):
        if self.comboBoxEpisode.currentIndex() >= 0:
            return self._episodes[self.comboBoxEpisode.currentIndex()]
        return None

    def get_sequence(self):
        if self.comboBoxSequence.currentIndex() >= 0:
            return self._sequences[self.comboBoxSequence.currentIndex()]
        return None

    def get_task_types(self):
        if len(self._user_task_types) > 0 and len(self._user_task_types) != len(self._task_types):
            return self._user_task_types
        return self._task_types

    def get_task_status(self):
        if len(self._user_task_status) > 0 and len(self._user_task_status) != len(self._task_status):
            return self._user_task_status
        return self._task_status

    def selection_changed(self, source, object):
        if "project_changed" in source:
            self.load_project_hierarchy()

        elif "episode_changed" in source:
            self.load_sequence()

    def project_changed(self, index):
        if index >= 0:
            self.signal.selection_changed.emit("project_changed", { 
                "project": self._projects[index],
                "is_loaded": self.is_loaded()
            } )

        ## write_log("project_changed", self._projects[index]["id"])

    def episode_changed(self, index):
        if index >= 0:
            self.signal.selection_changed.emit("episode_changed", { 
                "episode": self._episodes[index] 
            } )

        ## write_log("episode_changed", self._episodes[index]["id"])

    def sequence_changed(self, index):
        if index >= 0:
            self.signal.selection_changed.emit("sequence_changed", { 
                "sequence": self._sequences[index]["id"],
                "name": self._sequences[index]["name"]
            })

        ## write_log("sequence_changed", self._sequences[index]["id"])

    def task_types_changed(self, selection):
        if len(selection) >= 0:
            self.signal.selection_changed.emit("task_types_changed", { 
                "task_types": selection
            })

        ## write_log("sequence_changed", self._sequences[index]["id"])

    def status_codes_changed(self, selection):
        if len(selection) >= 0:
            self.signal.selection_changed.emit("status_codes_changed", { 
                "status_codes": selection
            })

        ## write_log("sequence_changed", self._sequences[index]["id"])

    def lock_ui(self, enabled):
        if not self.is_loaded():
            return False

        if enabled:
            self.comboBoxProject.setEnabled(False)
            self.comboBoxProject.blockSignals(True)

            self.comboBoxEpisode.setEnabled(False)
            self.comboBoxEpisode.blockSignals(True)

            self.comboBoxSequence.setEnabled(False)
            self.comboBoxSequence.blockSignals(True)

            self.toolButtonTaskTypes.setEnabled(False)
            self.toolButtonStatusTypes.setEnabled(False)

            self.progressBar.setMaximum(0)
        else:
            self.comboBoxProject.setEnabled(True)
            self.comboBoxProject.blockSignals(False)

            self.comboBoxEpisode.setEnabled(True)
            self.comboBoxEpisode.blockSignals(False)

            self.comboBoxSequence.setEnabled(True)
            self.comboBoxSequence.blockSignals(False)

            self.toolButtonTaskTypes.setEnabled(True)
            self.toolButtonStatusTypes.setEnabled(True)

            self.progressBar.setMaximum(1)

    def load_open_projects(self):
        self.lock_ui(True)

        loader = ProjectLoaderThread(self)
        loader.callback.loaded.connect(self.projects_loaded)

        self.threadpool.start(loader)        
        #loader.run()

    def load_project_hierarchy(self):
        self.lock_ui(True)
        
        self.comboBoxSequence.clear()

        loader = ProjectHierarchyLoaderThread(self, self.get_project())
        loader.callback.loaded.connect(self.hierarchy_loaded)

        self.threadpool.start(loader)     
        #loader.run()

    def load_sequence(self):
        self.lock_ui(True)

        self.comboBoxSequence.clear()
        self._sequences = []

        episode = self.get_episode()
        if not episode:
            return False

        if "sequences" in episode:
            sequences = episode["sequences"]

            for item in sequences:
                self._sequences.append(item)

            for item in self._sequences:
                self.comboBoxSequence.addItem(item["name"])

        self._status["sequences"] = True

        self.sequence_changed(self.comboBoxSequence.currentIndex())
        self.lock_ui(False)

    def hierarchy_loaded(self, results): 
        self.comboBoxEpisode.clear()
        self._task_types = []
        self._episodes = []        

        if len(results["task_types"]) * len(results["episodes"]) * len(results["status_codes"]) > 0:
            for item in results["task_types"]:
                if item not in self._task_types:
                    self._task_types.append(copy.copy(item))

            for item in results["status_codes"]:
                if item not in self._task_status:
                    self._task_status.append(copy.copy(item))

            for item in results["episodes"]:
                self._episodes.append(copy.copy(item))

            for item in self._episodes:
                self.comboBoxEpisode.addItem(item["name"])

            if len(self._episodes) > 0:
                self.comboBoxEpisode.setEnabled(True)
                self.episode_changed(self.comboBoxEpisode.currentIndex())
            else:
                self.comboBoxEpisode.setEnabled(False)

            if len(self._sequences) > 0:
                self.comboBoxSequence.setEnabled(True)
                self.sequence_changed(self.comboBoxSequence.currentIndex())            
            else:
                self.comboBoxSequence.setEnabled(True)

        self._status["episodes"] = True
        self.lock_ui(False)

    def projects_loaded(self, results): 
        ## write_log("[projects_loaded]")

        self._projects = []
        self._task_types = []

        if len(results) > 0:
            for item in results["projects"]:
                self._projects.append(copy.copy(item))

            for item in results["task_types"]:
                self._task_types.append(copy.copy(item))

            index = 0
            for item in self._projects:
                self.comboBoxProject.addItem(item["name"])

        self._status["projects"] = True
        self.load_project_hierarchy()


if __name__ == "__main__":
    password = load_keyring('swing', 'password', 'Not A Password')
    connect_to_server("user@example.com", password)
    
    app = QApplication(sys.argv)
    if darkStyle:
        # setup stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # or in new API
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))        

    nav = ProjectNavWidget()
    
    nav.show()
    nav.load_open_projects()

    sys.exit(app.exec_())
