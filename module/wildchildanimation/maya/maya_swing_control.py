import inspect
import sys
import traceback

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.utils as mutils

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from wildchildanimation.maya.swing_maya_control_ui import Ui_SwingControlWidget

from PySide2 import QtWidgets, QtCore

from wildchildanimation.studio.maya_studio_handlers import MayaStudioHandler
from wildchildanimation.gui.swing_gui import SwingGUI
from wildchildanimation.maya.maya_scene_data import SceneData
from wildchildanimation.maya.layout_control import LayoutControlDialog
from wildchildanimation.gui.background_workers import TaskFileInfoThread
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import friendly_string
from wildchildanimation.gui.background_workers import ProjectTypesLoader

mixinWindows = {}

class DockableBase(MayaQWidgetDockableMixin):
    """
    Convenience class for creating dockable Maya windows.
    """
    def __init__(self, controlName, **kwargs):
        super(DockableBase, self).__init__(**kwargs)
        self.setObjectName(controlName)   
                                    
    def show(self, *args, **kwargs):
        """
        Show UI with generated uiScript argument
        """
        modulePath = inspect.getmodule(self).__name__
        className = self.__class__.__name__
        super(DockableBase, self).show(dockable=True, uiScript="import {0}; {0}.{1}.display()".format(modulePath, className), **kwargs)
        
    @classmethod
    def _restoreUI(cls):
        """
        Internal method to restore the UI when Maya is opened.
        """
        # Create UI instance
        instance = cls()
        # Get the empty WorkspaceControl created by Maya
        workspaceControl = omui.MQtUtil.getCurrentParent()
        # Grab the pointer to our instance as a Maya object
        mixinPtr = omui.MQtUtil.findControl(instance.objectName())
        # Add our UI to the WorkspaceControl
        omui.MQtUtil.addWidgetToMayaLayout(int(mixinPtr), int(workspaceControl))
        # Store reference to UI
        global mixinWindows
        mixinWindows[instance.objectName()] = instance	

class SwingMayaUI(DockableBase, QtWidgets.QDialog, Ui_SwingControlWidget):   

    # singleton instance    
    ui_instance = None

    WINDOW_TITLE = "Treehouse: Swing"
    UI_NAME = "SwingMayaUI"

    projects = []
    episodes = []
    tasks = []
    task_types = None
    task = None
    task_info = None

    def __init__(self, parent=None):
        super(SwingMayaUI, self).__init__(parent=parent, controlName = SwingMayaUI.UI_NAME)

        print("SwingMayaUI::__init__")

        self.setObjectName(self.__class__.UI_NAME)
        self.setMinimumSize(600, 60)
        self.setupUi(self)

        self.create_connections()

        self.handler = MayaStudioHandler()
        self.set_enabled(False)

        self.toolButtonRefresh.setEnabled(True)
        self.toolButtonRefresh.setText("Connect")   

    @classmethod
    def display(cls):
        try:
            if not cls.ui_instance:
                cls.ui_instance = SwingMayaUI()

            cls.ui_instance._restoreUI()
        except:
            traceback.print_exc(file=sys.stdout)         

    def log_output(self, text):
        om.MGlobal.displayInfo(text)                  

    def create_connections(self):
        self.toolButtonRefresh.clicked.connect(self.connect_to_db)

        self.toolButtonSwing.clicked.connect(self.on_show_swing)
        self.toolButtonTask.clicked.connect(self.on_create)
        self.toolButtonPlayblast.clicked.connect(self.on_playblast)
        self.toolButtonBreakOut.clicked.connect(self.on_breakout_control)
        self.toolButtonPublish.clicked.connect(self.on_publish)
        self.toolButtonExport.clicked.connect(self.on_export)
        self.toolButtonSearch.clicked.connect(self.on_search)
        self.toolButtonEntityInfo.clicked.connect(self.on_entity_info)
        self.toolButtonUpdate.clicked.connect(self.on_update_scene)

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.comboBoxTaskType.currentIndexChanged.connect(self.task_type_changed)
        self.comboBoxTask.currentIndexChanged.connect(self.task_changed)

        self.checkBoxDoneTasks.clicked.connect(self.refresh_tasks)   
        # 

    def set_enabled(self, status):
        self.set_enabled_task_control(status)

        self.comboBoxProject.setEnabled(status)
        self.comboBoxEpisode.setEnabled(status)
        self.comboBoxTaskType.setEnabled(status)
        self.comboBoxTask.setEnabled(status)#   

    def set_enabled_task_control(self, status):
        self.toolButtonTask.setEnabled(status)
        self.toolButtonPublish.setEnabled(status)
        self.toolButtonPlayblast.setEnabled(status)
        self.toolButtonBreakOut.setEnabled(status)
        self.toolButtonExport.setEnabled(status)
        self.toolButtonSearch.setEnabled(status)
        self.toolButtonUpdate.setEnabled(status)
        
        self.toolButtonEntityInfo.setEnabled(status)

        self.lineEditSearch.setEnabled(status)                  

    def connect_to_db(self):
        self.toolButtonRefresh.setEnabled(False)
        if self.handler.validate_connection():
            try:
                self.load_projects()

                self.project_changed(self.comboBoxProject.currentIndex())
                self.episode_changed(self.comboBoxEpisode.currentIndex())
                self.toolButtonRefresh.setText("Refresh")
                self.log_output("Swing: Connected")    

                sd = SceneData()
                if sd.load_scene_descriptor():
                    try:
                        self.log_output("Loading Scene Descriptor")

                        project_id, episode_id, task_id = sd.load_task_data()
                        self.set_to_project(project_id)
                        self.set_to_episode(episode_id)
                        self.set_to_task(task_id)
                    except:
                        traceback.print_exc(file=sys.stdout)

                self.set_enabled(True)            
            except:
                traceback.print_exc(file=sys.stdout)
                self.toolButtonRefresh.setText("Retry")
        else:
            self.log_output("Swing: Check connection settings")
            
        self.toolButtonRefresh.setEnabled(True)        

    def set_to_project(self, id):
        idx = 0
        for idx in range(self.comboBoxProject.count()):
            if id == self.comboBoxProject.itemData(idx, QtCore.Qt.UserRole)["project_id"]:
                self.comboBoxProject.setCurrentIndex(idx)
                print("Found Project ID {}".format(id))
                break

    def set_to_episode(self, id):
        idx = 0
        for idx in range(self.comboBoxEpisode.count()):
            if id == self.comboBoxEpisode.itemData(idx, QtCore.Qt.UserRole)["episode_id"]:
                self.comboBoxEpisode.setCurrentIndex(idx)
                print("Found Episode ID {}".format(id))
                break

    def set_to_task(self, id):
        idx = 0
        for idx in range(self.comboBoxTask.count()):
            if id == self.comboBoxTask.itemData(idx, QtCore.Qt.UserRole)["task_id"]:
                self.comboBoxTask.setCurrentIndex(idx)#
                print("Found Task ID {}".format(id))
                break        

    def load_project_data(self, project_list):
        self.log_output("::load_project_data")

        self.projects = dict()
        for item in project_list:
            project = item['project']

            if not project in self.projects:
                self.projects[project] = {}

            project_item = self.projects[project]

            if not "project_id" in project_item:
                project_item["project_id"] = item["project_id"]

            if not "episodes" in project_item:
                project_item["episodes"] = []
                episode = {
                    "episode": "All",
                    "episode_id": "All"
                }
                project_item["episodes"].append(episode)

            project_episodes = project_item["episodes"]
            episode = {
                "episode": item["episode"],
                "episode_id": item["episode_id"]
            }
            project_episodes.append(episode)

        return self.projects

    def load_projects(self):
        self.comboBoxProject.blockSignals(True)
        self.comboBoxProject.setEnabled(False)
        self.comboBoxProject.clear()

        self.comboBoxEpisode.blockSignals(True)
        self.comboBoxEpisode.setEnabled(False)
        self.comboBoxEpisode.clear()

        self.comboBoxTaskType.blockSignals(True)
        self.comboBoxTaskType.setEnabled(False)
        self.comboBoxTaskType.clear()            

        self.comboBoxTask.blockSignals(True)
        self.comboBoxTask.setEnabled(False)
        self.comboBoxTask.clear()

        self.load_project_data(self.handler.load_project_episodes())

        # clear episodes and tasks on project load
        self.tasks = []              

        for item in self.projects.keys():
            self.comboBoxProject.addItem(item, userData = self.projects[item])    

        self.comboBoxProject.blockSignals(False)
        self.comboBoxProject.setEnabled(True)

        self.comboBoxEpisode.blockSignals(False)
        self.comboBoxEpisode.setEnabled(True)

        self.comboBoxTaskType.blockSignals(False)
        self.comboBoxTaskType.setEnabled(True)

        self.comboBoxTask.blockSignals(False)
        self.comboBoxTask.setEnabled(True)

        self.comboBoxProject.setCurrentIndex(0)
        ##self.task_types = self.handler.load_task_types()["results"]

    def project_changed(self, index):
        try:
            self.project = self.comboBoxProject.itemData(index)

            self.comboBoxEpisode.blockSignals(True)
            self.comboBoxEpisode.setEnabled(False)
            self.comboBoxEpisode.clear()

            self.comboBoxTaskType.blockSignals(True)
            self.comboBoxTaskType.setEnabled(False)
            self.comboBoxTaskType.clear()               

            self.comboBoxTask.blockSignals(True)
            self.comboBoxTask.setEnabled(False)
            self.comboBoxTask.clear()   

            # project = self.comboBoxProject.currentText()
            episodes = self.project["episodes"]

            loader = ProjectTypesLoader(self, self.project["project_id"])        
            loader.callback.loaded.connect(self.project_loaded)
            loader.run()            

            #self.comboBoxEpisode.addItem("MP", userData = {"episode": "all", "episode_id": "All"} )
            for item in episodes:
                self.comboBoxEpisode.addItem(item["episode"], userData = item)

        except:
            self.log_output("Error: project_changed:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)            

    def project_loaded(self, results):
        self.task_types = results["task_types"]
        self.task_status = results["task_status"]      

        self.comboBoxTaskType.blockSignals(True)        
        self.comboBoxTaskType.clear()

        task_type_all = {
            "name": "All",
            "task_type_id": "All"
        }        
        self.comboBoxTaskType.addItem("All", task_type_all)

        for item in self.task_types:
            self.comboBoxTaskType.addItem(item["name"], userData = item)

        self.comboBoxTaskType.blockSignals(False)    
        self.comboBoxTaskType.setEnabled(True)   

        self.comboBoxEpisode.blockSignals(False)
        self.comboBoxEpisode.setEnabled(True)

        self.comboBoxTask.blockSignals(False)
        self.comboBoxTask.setEnabled(True)

        self.comboBoxEpisode.setCurrentIndex(0)  
        ## self.episode_changed(self.comboBoxEpisode.currentIndex())              

    def episode_changed(self, index):

        self.refresh_tasks()

    def task_type_changed(self, index):

        self.refresh_tasks()

    def refresh_tasks(self):
        project = self.comboBoxProject.currentText()
        project_id = self.projects[project]["project_id"]

        episode_id = self.comboBoxEpisode.itemData(self.comboBoxEpisode.currentIndex())["episode_id"]    
        task_type = self.comboBoxTaskType.itemData(self.comboBoxTaskType.currentIndex())["name"]

        is_done = self.checkBoxDoneTasks.isChecked()

        self.comboBoxTask.blockSignals(True)
        self.comboBoxTask.setEnabled(False)
        self.comboBoxTask.clear()
        self.tasks = []
        
        items = self.handler.load_todo_tasks(project_id, episode_id, is_done)   

        for item in items:
            if not task_type == 'All':
                if not item["task_type"] == task_type:
                    continue # skip if not selected
            self.tasks.append(item)

        self.log_output("refresh_tasks: loaded {} tasks".format(len(self.tasks)))

        # add a blank task to force user to select via combobox
        self.comboBoxTask.addItem("", userData = {"project_id": project_id, "episode_id": episode_id, "task_id": None } )  

        for item in self.tasks:
            self.comboBoxTask.addItem(item["task"], userData = item)             

        self.comboBoxTask.blockSignals(False)
        self.comboBoxTask.setEnabled(len(self.tasks) > 0)

        self.comboBoxTask.setCurrentIndex(0)        
        self.task_changed(self.comboBoxTask.currentIndex())      

    def task_changed(self, index):
        if index < 0:
            return None

        item = self.comboBoxTask.itemData(index)
        task_id = item["task_id"]

        self.toolButtonTask.setEnabled(False)
        self.toolButtonPlayblast.setEnabled(False)
        self.toolButtonPublish.setEnabled(False)
        self.toolButtonExport.setEnabled(False)
        self.toolButtonEntityInfo.setEnabled(False)

        if not task_id:
            return 

        self.taskLoader = TaskFileInfoThread(parent = self, task = task_id, project_root=SwingSettings.get_instance().swing_root())
        self.taskLoader.callback.loaded.connect(self.on_task_loaded)
        QtCore.QThreadPool.globalInstance().start(self.taskLoader)            

    def on_task_loaded(self, results):
        self.task_info = results

        self.task = self.task_info["task"]
        self.task_dir = self.task_info["project_dir"]

        self.set_enabled_task_control(self.task is not None)

        #working_file = self.handler.get_task_sections(self.task)
        working_file = friendly_string("_".join(self.handler.get_task_sections(self.task)).lower())    
        self.log_output("Task: {} --> {}\{}.ma".format(self.task["id"], self.task_dir, working_file))

    def on_breakout_control(self):
        self.layoutControl = LayoutControlDialog(self, self.handler, self.task)
        self.layoutControl.show()        

    def on_breakout_control(self):
        self.layoutControl = LayoutControlDialog(self, self.handler, self.task)
        self.layoutControl.show()

    ### Studio Handlers
    def on_create(self):
        if not self.task_info:
            QtWidgets.QMessageBox.warning(self, 'Task not found', 'Please select a task before creating / loading')                  

            self.log_output("on_create::task_info not found")
            return 
        try:
            self.handler.on_create(parent = None, task = self.task)
        except:
            self.log_output("on_create:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_search(self):
        try:
            project_id = self.comboBoxProject.currentData()["project_id"]
            # entity = self.comboBoxTask.currentData()

            self.handler.on_search(parent = self, project = project_id, text = self.lineEditSearch.text() )
        except:
            self.log_output("on_search:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_publish(self):
        if not self.task_info:
            QtWidgets.QMessageBox.warning(self, 'Task not found', 'Please select a task before publishing')                  

            self.log_output("on_publish: Task not found")
            return 
        try:
            self.handler.on_publish(parent = None, task = self.task, task_types = self.task_types)        
        except:
            self.log_output("on_publish:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)            
        

    def on_playblast(self):
        if not self.task_info:
            QtWidgets.QMessageBox.warning(self, 'Task not found', 'Please select a task before playblasting')                  

            self.log_output("on_publish: Task not found")
            return         
        try:
            self.handler.on_playblast(parent = None, task = self.task)
        except:
            self.log_output("on_playblast:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_entity_info(self):
        try:
            task = self.comboBoxTask.currentData()

            self.handler.on_entity_info(parent = self, entity_id = task["entity_id"], task_types = self.task_types)
        except:
            self.log_output("on_entity_info:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)
            
    def on_show_swing(self):
        try:
            mutils.executeDeferred(lambda: SwingGUI.show_dialog(self.handler))
            #swing_loader = SwingLoader(self.handler)
            #self.threadpool.start(swing_loader)
            # 
        except:
            self.log_output("on_show_swing:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_export(self):
        try:
            task = self.comboBoxTask.currentData()

            self.handler.on_export(parent = self, task = task)
        except:
            self.log_output("on_export:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_update_scene(self):
        self.handler.on_update_scene(parent = self)
    

