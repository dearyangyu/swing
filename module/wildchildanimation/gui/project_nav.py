# -*- coding: utf-8 -*-

import sys

# ==== auto Qt load ====
try:
    from PySide2.QtWidgets import QApplication, QWidget
    from PySide2.QtCore import Signal as pyqtSignal
    from PySide2.QtCore import QObject, QThreadPool
    qtMode = 0
except ImportError:
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtCore import pyqtSignal
    from PyQt5.QtCore import QObject, QThreadPool
    qtMode = 1

# === theme it dark
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False

from wildchildanimation.gui.swing_utils import connect_to_server, load_keyring, set_button_icon, write_log
from wildchildanimation.gui.background_workers import ProjectLoaderThread, ProjectShotLoader, ProjectTypesLoader
from wildchildanimation.gui.project_nav_widget import Ui_ProjectNavWidget
from wildchildanimation.gui.entity_select import *
from wildchildanimation.gui.settings import SwingSettings

class NavigationChangedSignal(QObject):

    # setting up custom signal
    selection_changed = pyqtSignal(str, object) 

class ProjectNavWidget(QWidget, Ui_ProjectNavWidget):

    _task_types = []
    _user_task_types = []

    _software = []

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
        self.read_settings()

        set_button_icon(self.toolButtonRefresh, "../resources/fa-free/solid/sync-solid.svg")
        self.toolButtonRefresh.clicked.connect(self.load_open_projects)

        self.toolButtonTaskTypes.clicked.connect(self.select_task_types)
        set_button_icon(self.toolButtonTaskTypes, "../resources/fa-free/solid/list.svg")

        self.toolButtonStatusTypes.clicked.connect(self.select_status_types)
        set_button_icon(self.toolButtonStatusTypes, "../resources/fa-free/solid/tasks.svg")        

        self.signal = NavigationChangedSignal()
        #self.signal.selection_changed.connect(self.selection_changed)

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.comboBoxSequence.currentIndexChanged.connect(self.sequence_changed)

        # fix for MacOS combo dropdown 
        delegate = QtWidgets.QStyledItemDelegate()
        self.comboBoxProject.setItemDelegate(delegate)        
        self.comboBoxEpisode.setItemDelegate(delegate)        
        self.comboBoxSequence.setItemDelegate(delegate)        

        self.toggle_filter_buttons()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        self._user_task_types = self.settings.value("task_types", [])
        self._user_task_status = self.settings.value("status_codes", [])
        self.last_project_id = self.settings.value("last_project", -1)
        self.settings.endGroup()            

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        project = self.get_project()
        if project:
            self.settings.setValue("last_project", project["project_id"])
        else:
            self.settings.setValue("last_project", "")

        self.settings.endGroup()  #  
        self.settings.sync()

    def is_task_types_filtered(self):
        return len(self._user_task_types) > 0 and len(self._user_task_types) != len(self._task_types)

    def is_status_types_filtered(self):
        return len(self._user_task_status) > 0 and len(self._user_task_status) != len(self._task_status)

    def toggle_filter_buttons(self):
        if self.is_task_types_filtered():
            self.toolButtonTaskTypes.setStyleSheet("background-color: #505569;")            
        else:
            self.toolButtonTaskTypes.setStyleSheet(None)

        if self.is_status_types_filtered():
            self.toolButtonStatusTypes.setStyleSheet("background-color: #505569;")            
        else:
            self.toolButtonStatusTypes.setStyleSheet(None)

    def select_task_types(self):
        dialog = EntitySelectDialog(self, "Select Task Types")
        dialog.load(self._task_types, self._user_task_types)
        if dialog.exec_():
            self._user_task_types = dialog.get_selection()
            self.task_types_changed(self._user_task_types)
        self.toggle_filter_buttons()

    def select_status_types(self):
        dialog = EntitySelectDialog(self, "Select Status Codes")
        dialog.load(self._task_status, self._user_task_status)
        if dialog.exec_():
            self._user_task_status = dialog.get_selection()
            self.status_codes_changed(self._user_task_status)
        self.toggle_filter_buttons()

    def is_loaded(self):
        return self._status["projects"] and self._status["episodes"] and self._status["sequences"]

    def get_project(self):
        return self.comboBoxProject.currentData()

    def set_project(self, index):
        self.comboBoxProject.setCurrentIndex(index)
        self.project_changed(index)

    def get_episode(self):
        return self.comboBoxEpisode.currentData()

    def set_episode(self, index):
        self.comboBoxEpisode.setCurrentIndex(index)
        self.episode_changed(index)

    def get_sequence(self):
        return self.comboBoxSequence.currentData()

    def get_task_types(self):
        if len(self._user_task_types) > 0 and len(self._user_task_types) != len(self._task_types):
            return self._user_task_types
        return self._task_types

    def get_task_status(self):
        if len(self._user_task_status) > 0 and len(self._user_task_status) != len(self._task_status):
            return self._user_task_status
        return self._task_status

    def get_user_task_status(self):
        items = []
        for item in self._task_status:
            if item["is_artist_allowed"]:
                items.append(item)
        return items

    def get_software(self):
        return self._software
        ## write_log("project_changed", self._projects[index]["id"])

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

    def project_hierarchy_loaded(self):
        self.signal.selection_changed.emit("project_hierarchy_loaded", { 
            "status": "OK"
        })

        ## write_log("sequence_changed", self._sequences[index]["id"])        

    def set_enabled(self, enabled):
        ## print("projectNav is_locked {} should_lock {} is_loaded {}".format(self.locked, enabled, self.is_loaded()))

        self.comboBoxProject.setEnabled(enabled)
        self.comboBoxEpisode.setEnabled(enabled)
        self.comboBoxSequence.setEnabled(enabled)
        self.toolButtonTaskTypes.setEnabled(enabled)
        self.toolButtonStatusTypes.setEnabled(enabled)

    def load_open_projects(self):
        #self.comboBoxProject.clear()
        #self.comboBoxEpisode.clear()        
        #self.comboBoxSequence.clear()

        loader = ProjectLoaderThread(self)
        loader.callback.loaded.connect(self.projects_loaded)
        
        self.set_enabled(False)
        self.threadpool.start(loader)  
        ##loader.run()

    def projects_loaded(self, results): 
        try:
            self._software = results["software"]
            ##self._task_types = results["task_types"]
            ##self._task_status = results["task_status"]

            project_dict = {}
            for item in results["projects"]:
                project_id = item["project_id"]
                if not project_id in project_dict:
                    project_dict[project_id] = { "project_id": project_id, "project": item["project"], "episodes": [] }

                project = project_dict[project_id]
                project["episodes"].append(item)

            self._projects = []
            for item in project_dict:
                self._projects.append(project_dict[item])

            self._status["projects"] = True
            self._status["episodes"] = True

            self.comboBoxProject.blockSignals(True)
            self.comboBoxProject.clear()

            found = None
            index = 0
            for item in self._projects:
                self.comboBoxProject.addItem(item["project"], userData = item)
                if item["project_id"] == self.last_project_id:
                    found = index
                index += 1

            self.comboBoxProject.blockSignals(False)

            self.comboBoxEpisode.clear()
            self.comboBoxSequence.clear()

            if found:
                self.set_project(found)
            else:
                self.set_project(self.comboBoxProject.currentIndex())
            
        except:
            print("Error loading project properties: Please check connection settings")
            
        self.set_enabled(True)

    def project_changed(self, index):
        project = self.comboBoxProject.itemData(index)

        if not project:
            write_log("Error: No open project could be loaded, please check settings")
            write_log("Server: {}".format(SwingSettings.get_instance().swing_server()))
            write_log("Artist: {}".format(SwingSettings.get_instance().swing_user()))

            return False


        loader = ProjectTypesLoader(self, project["project_id"])        
        loader.callback.loaded.connect(self.project_loaded)
        loader.run()

        self.comboBoxEpisode.clear()
        self.comboBoxSequence.clear()

        self.comboBoxEpisode.blockSignals(True)

        # Add Main Pack Episode placeholder for Asset Tasks
        self.comboBoxEpisode.addItem("MP", userData = {"episode": "all", "episode_id": "All"} )
        if "episodes" in project:
            episodes = project["episodes"]
            for item in episodes:
                self.comboBoxEpisode.addItem(item["episode"], userData = item)
            
        self.comboBoxEpisode.blockSignals(False)

        self.comboBoxEpisode.setCurrentIndex(0)   
        self.episode_changed(self.comboBoxProject.currentIndex())
        ## self.sequence_changed(self.comboBoxSequence.currentIndex())   
        # 

    def project_loaded(self, results):
        self._task_types = results["task_types"]
        self._task_status = results["task_status"]        


    def episode_changed(self, index):
        episode = self.get_episode()

        if episode is None:
            return

        loader = ProjectShotLoader(episode["episode_id"])
        loader.callback.loaded.connect(self.sequence_loaded)

        loader.run()
        if index >= 0:
            self.signal.selection_changed.emit("episode_changed", { 
                "episode": self.get_episode()
            } )

    def sequence_loaded(self, results):
        sequence_dict = {}

        for item in results:
            sequence_id = item["sequence_id"]

            if not sequence_id in sequence_dict:
                sequence_dict[sequence_id] = { "sequence_id": item["sequence_id"], "sequence": item["sequence"], "episode_id": item["episode_id"] }

            sequence = sequence_dict[sequence_id]
            if not "shots" in sequence:
                sequence["shots"] = []

            shots = sequence["shots"]
            shots.append(item)

        self.comboBoxSequence.blockSignals(True)
        self.comboBoxSequence.clear()
        self.comboBoxSequence.addItem("All", userData = {"sequence": "all", "sequence_id": "All"})
        for item in sequence_dict.values():
            self.comboBoxSequence.addItem(item["sequence"], userData = item)
        self.comboBoxSequence.blockSignals(False)                

        self._status["sequences"] = True

        self.set_enabled(True)

        self.comboBoxSequence.setCurrentIndex(0)
        self.sequence_changed(self.comboBoxSequence.currentIndex())

    def sequence_changed(self, index):
        if index >= 0:
            sequence = self.get_sequence()
            self.signal.selection_changed.emit("sequence_changed", { 
                "sequence": sequence, 
                "name": sequence["sequence"]
            })

    def on_close(self, event):
        self.write_settings()


if __name__ == "__main__":
    password = load_keyring('swing', 'password', 'Not A Password')
    connect_to_server("user@example.com", password)
    
    app = QApplication(sys.argv)
    if darkStyle:
        # setup stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet())
        # or in new API
        ## app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))        

    nav = ProjectNavWidget()
    
    nav.show()
    nav.load_open_projects()

    sys.exit(app.exec_())
