import maya.cmds as mc
import maya.OpenMaya as om

from wildchildanimation.gui.settings import SwingSettings

from wildchildanimation.maya.maya_shelf import _shelf
from wildchildanimation.gui.swing_gui import SwingGUI

class SwingShelf(_shelf):

    _project = None
    _project_button = None

    _episode = None
    _episode_button = None

    _task = None
    _task_button = None

    _load_projects = '''
from wildchildanimation.studio.maya_studio_handlers import MayaStudioHandler
wildchildanimation.SwingGUI.show_dialog(MayaStudioHandler())
    '''

    _run_swing = '''
from wildchildanimation.studio.maya_studio_handlers import MayaStudioHandler
wildchildanimation.SwingGUI.show_dialog(MayaStudioHandler())
    '''

    _playblast = '''
swing_playblast_dialog = wildchildanimation.gui.swing_playblast.SwingPlayblastUi()
swing_playblast_dialog.show()
    '''    

    def __init__(self, name, iconPath):
        super().__init__(name=name, iconPath=iconPath)
        self.log_output("Loading {}".format(self.name))

    def build(self):
        self._project_button = self.addButon(label="Project", icon = "toolbar/button_pr.png", command = self.load_projects, width=100)        
        self._episode_button = self.addButon(label="Ep", icon = "toolbar/button_ep.png", command = SwingShelf._run_swing, width=100)
        self._task_button = self.addButon(label="Task", icon = "toolbar/button_ta.png", command = SwingShelf._playblast, width=100)        

    def log_output(self, text):
        om.MGlobal.displayInfo(text)
        print("[info] {}".format(text))        

    def validate_connection(self):
        if not SwingGUI.get_instance().connected and not SwingGUI.get_instance().connect_to_server():
            self.log_output("opening connection settings")
            return SwingGUI.get_instance().open_connection_settings()
        return True

# #         self.addButon(label="button1")
# #         self.addButon("button2")
# #         self.addButon("popup")

# #         p = mc.popupMenu(b=1)
# #         self.addMenuItem(p, "popupMenuItem1")
# #         self.addMenuItem(p, "popupMenuItem2")

# #         sub = self.addSubMenu(p, "subMenuLevel1")
# #         self.addMenuItem(sub, "subMenuLevel1Item1")

# #         sub2 = self.addSubMenu(sub, "subMenuLevel2")
# #         self.addMenuItem(sub2, "subMenuLevel2Item1")
# #         self.addMenuItem(sub2, "subMenuLevel2Item2")
# #         self.addMenuItem(sub, "subMenuLevel1Item2")

# #         self.addMenuItem(p, "popupMenuItem3")

# #         self.addButon("button3")        

    def load_projects(self):
        self.log_output("loading projects")

        if not self.validate_connection():
            self.log_output("connection error")
            return

        popup = mc.popupMenu(b=1)
        for item in SwingGUI.get_instance().nav._projects:
            self.addMenuItem(popup, item["name"], command = lambda x: self.project_selected(item))
            self.log_output("Added Project: {}".format(item["name"]))   

        sub = self.addSubMenu(popup, "Selection")

        self.addMenuItem(sub, "Project Selection")         
        self.addMenuItem(popup, "Popup Selection")  

    def load_episodes(self):
        self.log_output("loading episodes")

        if not self.validate_connection():
            self.log_output("connection error")
            return

        popup = mc.popupMenu(b=1)

        for item in SwingGUI.get_instance().nav._episodes:
            self.addMenuItem(popup, item["name"], command = lambda x: self.episode_selected(item))
            self.log_output("Added Episode: {}".format(item["name"]))            

        self.addMenuItem(popup, "Episodes")              

    def load_tasks(self):
        self.log_output("loading tasks")

        if not self.validate_connection():
            self.log_output("connection error")
            return

        popup = mc.popupMenu(b=1)

        for item in SwingGUI.get_instance().nav.tasks:
            self.addMenuItem(popup, item["name"], command = lambda x: self.task_selected(item))

        self.addMenuItem(popup, "Episodes")               

    def project_selected(self, project, *args):
        self._project = project
        self.log_output("Project {}".format(self._project["name"]))

        self.load_episodes()

    def episode_selected(self, episode, *args):
        self._episode = episode
        self.log_output("Episode {}".format(self._episode["name"]))

        self.load_tasks()    

    def task_selected(self, task, *args):
        self._task = task
        self.log_output("Task {}".format(self._task["name"]))




# ###################################################################################
# '''This is an example shelf.'''
# # class customShelf(_shelf):
# #     def build(self):
# #         self.addButon(label="button1")
# #         self.addButon("button2")
# #         self.addButon("popup")
# #         p = mc.popupMenu(b=1)
# #         self.addMenuItem(p, "popupMenuItem1")
# #         self.addMenuItem(p, "popupMenuItem2")
# #         sub = self.addSubMenu(p, "subMenuLevel1")
# #         self.addMenuItem(sub, "subMenuLevel1Item1")
# #         sub2 = self.addSubMenu(sub, "subMenuLevel2")
# #         self.addMenuItem(sub2, "subMenuLevel2Item1")
# #         self.addMenuItem(sub2, "subMenuLevel2Item2")
# #         self.addMenuItem(sub, "subMenuLevel1Item2")
# #         self.addMenuItem(p, "popupMenuItem3")
# #         self.addButon("button3")
# # customShelf()
# ###################################################################################