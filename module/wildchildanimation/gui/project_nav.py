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

from swing_utils import connect_to_server, write_log, load_keyring, load_settings, save_settings
from background_workers import ProjectLoaderThread, ProjectHierarchyLoaderThread
from project_nav_widget import Ui_ProjectNavWidget


class NavigationChangedSignal(QObject):

    # setting up custom signal
    selection_changed = pyqtSignal(str, object) 

class ProjectNavWidget(QWidget, Ui_ProjectNavWidget):

    _projects = []
    _episodes = []
    _sequences = []
    _task_types = []
    
    def __init__(self):
        super(ProjectNavWidget, self).__init__(None) # Call the inherited classes __init__ method
        self.threadpool = QThreadPool.globalInstance()

        self.setupUi(self)
        self.toolButtonRefresh.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))

        self.signal = NavigationChangedSignal()
        self.signal.selection_changed.connect(self.selection_changed)

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.comboBoxSequence.currentIndexChanged.connect(self.sequence_changed)

    def get_project(self):
        return self._projects[self.comboBoxProject.currentIndex()]

    def get_episode(self):
        return self._episodes[self.comboBoxEpisode.currentIndex()]

    def get_sequence(self):
        return self._sequences[self.comboBoxSequence.currentIndex()]

    def selection_changed(self, source, object):
        if "project_changed" in source:
            self.load_project_hierarchy()
        elif "episode_changed" in source:
            self.load_sequence()

    def project_changed(self, index):
        self.signal.selection_changed.emit("project_changed", self._projects[index])

        write_log("project_changed", self._projects[index])

    def episode_changed(self, index):
        self.signal.selection_changed.emit("episode_changed", self._episodes[index])

        write_log("episode_changed", self._episodes[index])

    def sequence_changed(self, index):
        self.signal.selection_changed.emit("sequence_changed", self._sequences[index]["id"], self._sequences[index]["name"])

        write_log("sequence_changed", self._sequences[index])

    def lock_ui(self, enabled):
        if enabled:
            self.comboBoxProject.setEnabled(False)
            self.comboBoxEpisode.setEnabled(False)
            self.comboBoxSequence.setEnabled(False)
            self.progressBar.setMaximum(0)
        else:
            self.comboBoxProject.setEnabled(True)
            self.comboBoxEpisode.setEnabled(True)
            self.comboBoxSequence.setEnabled(True)
            self.progressBar.setMaximum(1)

    def load_open_projects(self):
        self.lock_ui(True)

        loader = ProjectLoaderThread(self)
        loader.callback.loaded.connect(self.projects_loaded)

        self.threadpool.start(loader)        

    def load_project_hierarchy(self):
        self.lock_ui(True)
        
        self.comboBoxSequence.clear()

        loader = ProjectHierarchyLoaderThread(self, self.get_project())
        loader.callback.loaded.connect(self.hierarchy_loaded)

        self.threadpool.start(loader)     

    def load_sequence(self):
        self.lock_ui(True)
        self.comboBoxSequence.clear()

        episode = self.get_episode()

        if "sequences" in episode:
            sequences = episode["sequences"]

            for item in sequences:
                self._sequences.append(item)

            for item in self._sequences:
                self.comboBoxSequence.addItem(item["name"])

        self.lock_ui(False)

    def hierarchy_loaded(self, data): 
        self.comboBoxEpisode.clear()

        self._episodes = []
        for item in data:
            self._episodes.append(copy.copy(item))

        for item in self._episodes:
            self.comboBoxEpisode.addItem(item["name"])

        self.lock_ui(False)

    def projects_loaded(self, results): 
        write_log("[projects_loaded]")

        self._projects = []
        for item in results["projects"]:
            self._projects.append(copy.copy(item))

        self._task_types = []
        for item in results["task_types"]:
            self._task_types.append(copy.copy(item))

        index = 0
        for item in self._projects:
            self.comboBoxProject.addItem(item["name"])

        self.lock_ui(False)


if __name__ == "__main__":
    password = load_keyring('swing', 'password', 'Not A Password')
    connect_to_server("showadmin@digitalevolution.co.za", password)
    
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
