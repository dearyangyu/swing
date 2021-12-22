# -*- coding: utf-8 -*-
# Maya Widget control for Treehouse: Swing
#
import sys
import traceback

#import maya.cmds as cmds
#import maya.OpenMaya as om
#import maya.OpenMayaUI as omui
import maya.utils as mutils

from shiboken2 import wrapInstance, getCppPointer
from wildchildanimation.maya.layout_control import LayoutControlDialog
from wildchildanimation.gui.background_workers import TaskFileInfoThread
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import friendly_string

# ==== auto Qt load ====
try:
    from PySide2 import QtWidgets, QtCore
    qtMode = 0
except ImportError:
    from PyQt5 import QtWidgets, QtCore
    qtMode = 1

from wildchildanimation.maya.workspace_control import WorkspaceControl
from wildchildanimation.studio.maya_studio_handlers import MayaStudioHandler, maya_main_window
from wildchildanimation.maya.swing_maya_control_ui import Ui_SwingControlWidget

from wildchildanimation.gui.swing_gui import SwingGUI
from wildchildanimation.maya.maya_scene_data import SceneData

class SwingMayaUI(QtWidgets.QWidget, Ui_SwingControlWidget):

    WINDOW_TITLE = "Treehouse: Swing"
    UI_NAME = "SwingMayaUI"

    ui_instance = None
    handler = None

    projects = []
    episodes = []
    tasks = []
    task_types = None
    task = None
    task_info = None

    @classmethod
    def display(cls):
        try:
            if cls.ui_instance:
                cls.ui_instance.show_workspace_control()
            else:
                cls.ui_instance = SwingMayaUI()
        except:
            traceback.print_exc(file=sys.stdout)

    @classmethod
    def get_workspace_control_name(cls):
        return "{0}".format(cls.UI_NAME)

    def __init__(self, parent = maya_main_window()):
    #def __init__(self, parent = None):
        # maya_main_window = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        super(SwingMayaUI, self).__init__(parent)

        self.setObjectName(self.__class__.UI_NAME)
        self.setMinimumSize(600, 60)
        self.create_workspace_control()
        self.setupUi(self)

        self.create_connections()

        self.handler = MayaStudioHandler()
        self.set_enabled(False)

        self.toolButtonRefresh.setEnabled(True)
        self.toolButtonRefresh.setText("Connect")

    def set_enabled_task_control(self, status):
        self.toolButtonTask.setEnabled(status)
        self.toolButtonPublish.setEnabled(status)
        self.toolButtonPlayblast.setEnabled(status)
        self.toolButtonBreakOut.setEnabled(status)
        self.toolButtonExport.setEnabled(status)
        self.toolButtonSearch.setEnabled(status)
        self.toolButtonEntityInfo.setEnabled(status)

        self.lineEditSearch.setEnabled(status)        

    def set_enabled(self, status):
        self.set_enabled_task_control(status)

        self.comboBoxProject.setEnabled(status)
        self.comboBoxEpisode.setEnabled(status)
        self.comboBoxTask.setEnabled(status)

    def selection_changed(self, source, selection): 
        self.workspace_control_instance.log_output("selection_changed {} {}".format(source, selection))

    def create_connections(self):
        self.toolButtonSwing.clicked.connect(self.on_show_swing)

        self.toolButtonRefresh.clicked.connect(self.connect)
        self.toolButtonTask.clicked.connect(self.on_create)

        #self.toolButtonPlayblast.clicked.connect(SwingGUI.get_instance().playblast_dialog)
        self.toolButtonPlayblast.clicked.connect(self.on_playblast)
        self.toolButtonPublish.clicked.connect(self.on_publish)
        self.toolButtonExport.clicked.connect(self.on_export)

        self.toolButtonSearch.clicked.connect(self.on_search)
        self.toolButtonEntityInfo.clicked.connect(self.on_entity_info)

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.comboBoxTask.currentIndexChanged.connect(self.task_changed)

        self.toolButtonBreakOut.clicked.connect(self.on_breakout_control)

    def create_workspace_control(self):
        self.workspace_control_instance = WorkspaceControl(self.get_workspace_control_name())
        self.workspace_control_instance.log_output("Swing: Loaded WorkspaceControl")

        if self.restore_workspace_control():
            self.workspace_control_instance.log_output("Swing: Found existing workspace control, restoring")            
        else:
            self.workspace_control_instance.log_output("Swing: Creating new workspace control instance")            
            self.workspace_control_instance.create(self.WINDOW_TITLE, self, ui_script='from wildchildanimation.maya.maya_swing_control import SwingMayaUI\nSwingMayaUI()\n')

    def restore_workspace_control(self):
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
            return True
        return False        

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)
        # self.connect()

    def connect(self):
        self.toolButtonRefresh.setEnabled(False)
        if self.handler.validate_connection():
            try:
                self.load_projects()

                self.project_changed(self.comboBoxProject.currentIndex())
                self.episode_changed(self.comboBoxEpisode.currentIndex())
                self.toolButtonRefresh.setText("Refresh")
                self.workspace_control_instance.log_output("Swing: Connected")    

                sd = SceneData()
                if sd.load_scene_descriptor():
                    try:
                        print("Loading Scene Descriptor")

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
            self.workspace_control_instance.log_output("Swing: Check connection settings")
            
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
        self.workspace_control_instance.log_output("::load_project_data")

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

        self.comboBoxTask.blockSignals(True)
        self.comboBoxTask.setEnabled(False)
        self.comboBoxTask.clear()

        self.load_project_data(self.handler.load_project_episodes())

        # clear episodes and tasks on project load
        self.tasks = []              

        for item in self.projects.keys():
            ## self.workspace_control_instance.log_output("Item: {}".format(item))
            self.comboBoxProject.addItem(item, userData = self.projects[item])    

        self.comboBoxProject.blockSignals(False)
        self.comboBoxProject.setEnabled(True)

        self.comboBoxEpisode.blockSignals(False)
        self.comboBoxEpisode.setEnabled(True)

        self.comboBoxTask.blockSignals(False)
        self.comboBoxTask.setEnabled(True)

        self.comboBoxProject.setCurrentIndex(0)
        self.task_types = self.handler.load_task_types()["results"]

    def project_changed(self, index):
        try:
            self.comboBoxEpisode.blockSignals(True)
            self.comboBoxEpisode.setEnabled(False)
            self.comboBoxEpisode.clear()

            self.comboBoxTask.blockSignals(True)
            self.comboBoxTask.setEnabled(False)
            self.comboBoxTask.clear()   

            project = self.comboBoxProject.currentText()
            episodes = self.projects[project]["episodes"]

            #self.comboBoxEpisode.addItem("MP", userData = {"episode": "all", "episode_id": "All"} )
            for item in episodes:
                self.comboBoxEpisode.addItem(item["episode"], userData = item)

            self.comboBoxEpisode.blockSignals(False)
            self.comboBoxEpisode.setEnabled(True)

            self.comboBoxTask.blockSignals(False)
            self.comboBoxTask.setEnabled(True)

            self.comboBoxEpisode.setCurrentIndex(0)  
            self.episode_changed(self.comboBoxEpisode.currentIndex())              
        except:
            self.workspace_control_instance.log_error("project_changed:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)            

    def episode_changed(self, index):
        try:
            self.comboBoxTask.blockSignals(True)
            self.comboBoxTask.setEnabled(False)
            self.comboBoxTask.clear()           

            project = self.comboBoxProject.currentText()
            project_id = self.projects[project]["project_id"]
            episode_id = self.comboBoxEpisode.itemData(index)["episode_id"] 

            self.tasks = self.handler.load_todo_tasks(project_id, episode_id)

            # add a blank task to force user to select via combobox
            self.comboBoxTask.addItem("", userData = {"project_id": project_id, "episode_id": episode_id, "task_id": None } )  

            for item in self.tasks:
                self.comboBoxTask.addItem(item["task"], userData = item)             

            self.comboBoxTask.blockSignals(False)
            self.comboBoxTask.setEnabled(True)

            self.comboBoxTask.setCurrentIndex(0)        
            self.task_changed(self.comboBoxTask.currentIndex())        
        except:
            self.workspace_control_instance.log_error("episode_changed:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)            


    def on_task_loaded(self, results):
        self.task_info = results

        self.task = self.task_info["task"]
        self.task_dir = self.task_info["project_dir"]

        self.toolButtonTask.setEnabled(True)
        self.toolButtonPlayblast.setEnabled(True)
        self.toolButtonPublish.setEnabled(True)
        self.toolButtonExport.setEnabled(True)
        self.toolButtonEntityInfo.setEnabled(True)

        #working_file = self.handler.get_task_sections(self.task)
        working_file = friendly_string("_".join(self.handler.get_task_sections(self.task)).lower())    
        self.workspace_control_instance.log_output("Task: {} --> {}\{}.ma".format(self.task["id"], self.task_dir, working_file))

    def task_changed(self, index):
        item = self.comboBoxTask.itemData(index)
        #self.workspace_control_instance.log_output("Task: {}".format(item))
        task_id = item["task_id"]

        self.toolButtonTask.setEnabled(False)
        self.toolButtonPlayblast.setEnabled(False)
        self.toolButtonPublish.setEnabled(False)
        self.toolButtonExport.setEnabled(False)
        self.toolButtonEntityInfo.setEnabled(False)

        if not task_id:
            #self.workspace_control_instance.log_output("Nothing selected: {}".format(item))
            #self.toolButtonTask.setToolTip("")
            return 

        self.taskLoader = TaskFileInfoThread(parent = self, task = task_id, project_root=SwingSettings.get_instance().swing_root())
        self.taskLoader.callback.loaded.connect(self.on_task_loaded)
        QtCore.QThreadPool.globalInstance().start(self.taskLoader)

        '''        
        results = {
            "task": task,
            "task_dir": task_dir,
            "project_dir": resolve_content_path(task_dir, self.project_root),
            "project": project
        }
        '''  

    def on_breakout_control(self):
        self.layoutControl = LayoutControlDialog(self, self.handler, self.task)
        self.layoutControl.show()


    ### Studio Handlers
    def on_create(self):
        if not self.task_info:
            self.workspace_control_instance.log_output("on_create::task_info not found")
            return 
        try:
            #self.workspace_control_instance.log_output("handler: {}".format(self.task_info))
            self.handler.on_create(parent = None, task = self.task)
        except:
            self.workspace_control_instance.log_output("on_create:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_search(self):
        try:
            project_id = self.comboBoxProject.currentData()["project_id"]
            entity = self.comboBoxTask.currentData()

            self.handler.on_search(parent = self.workspace_control_instance, project = project_id, text = self.lineEditSearch.text() )
        except:
            self.workspace_control_instance.log_output("on_search:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_publish(self):
        if not self.task_info:
            self.workspace_control_instance.log_output("on_publish: Task not found")
            return 
        try:
            self.handler.on_publish(parent = None, task = self.task, task_types = self.task_types)        
        except:
            self.workspace_control_instance.log_output("on_publish:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)            
        

    def on_playblast(self):
        if not self.task_info:
            self.workspace_control_instance.log_output("on_publish: Task not found")
            return         
        try:
            self.handler.on_playblast(parent = None, task = self.task)
        except:
            self.workspace_control_instance.log_output("on_playblast:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_entity_info(self):
        try:
            task = self.comboBoxTask.currentData()

            self.handler.on_entity_info(parent = self.workspace_control_instance, entity_id = task["entity_id"], task_types = self.task_types)
        except:
            self.workspace_control_instance.log_output("on_entity_info:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)
            
    def on_show_swing(self):
        try:
            mutils.executeDeferred(lambda: SwingGUI.show_dialog(self.handler))
            #swing_loader = SwingLoader(self.handler)
            #self.threadpool.start(swing_loader)
            # 
        except:
            self.workspace_control_instance.log_output("on_show_swing:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def on_export(self):
        try:
            task = self.comboBoxTask.currentData()

            self.handler.on_export(parent = self.workspace_control_instance, task = task)
        except:
            self.workspace_control_instance.log_output("on_export:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

