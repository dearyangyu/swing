# -*- coding: utf-8 -*-
# 
# ==== auto Qt load ====
import os

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.background_workers import ProjectEpisodeLoader, ProjectShotLoader, TaskTypeLoader, ToDoLoader
from wildchildanimation.gui.swing_utils import connect_to_server, friendly_string

try:
    from PySide2 import QtCore
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    qtMode = 1    

class StudioInterface(QtCore.QObject):

    NAME = "StudioInterface"
    VERSION = "0.0.4"    

    def __init__(self):
        super(StudioInterface, self).__init__()

    '''
        Naming Lookups
    '''
    # ==== auto Qt load ====
    ASSET_TYPE_LOOKUP = {
        "Camera": "cam",
        "Character": "chr",
        "Environment": "env",
        "Library": "lib",
        "Model": "mod",
        "Prop": "prp",
        "Rig": "rig",
        "Test": "test"
    }

    FRAME_RANGE_PRESETS = [
        "Render",
        "Playback",
        "Animation",
        "Custom"
    ]        


    SUPPORTED_TYPES = [ ]
    UNARCHIVE_TYPES = [ ".zip", ".rar" ]

    def get_param(self, option, value):
        # return key / value pairs
        return False

    def log_error(self, text):
        ### log error
        return False

    def log_warning(self, text):
        ### log warning
        return False

    def log_output(self, text):
        ### log output
        return False

    def set_globals(self, **kwargs):
        ### set global parameters
        return False

    def list_unresolved(self):
        ### return a json list of unresolved references
        return False

    def import_reference(self, **kwargs):
        # tries to import the file specified in source into the currently open scene
        return False
    
    def load_file(self, **kwargs):
        # tries to import the file specified in source into the currently open scene
        return False

    def import_file(self, **kwargs):
        # tries to import the file specified in source into the currently open scene
        return False     

    def import_reference(self, **kwargs):
        # tries to import the file specified in source into the currently open scene
        return False           

    def on_save(self, **kwargs):
        # return the currently open file
        return False

    def on_create(self, **kwargs):

        return False

    # 
    def on_show_swing(self):
        """Show Swing GUI
        """
        return False

    def on_load(self, **kwargs):
        """Call Swing Loader
        """        
        return False

    def on_search(self, **kwargs):
        """Search Treehouse for files containg 'text'

        Args:
            parent (QtCore.QObject): Parent object
            project (str or dict): Project to search
            entity (str or dict): Optional - Owner for Downloads 
            text (str): Optional - Text to search for
            task_types (list): Optional - Task types to include in search or none for all
            status_types (list): Optional - Status types to include in search or none for all
        """
        return False

    def on_export(self, **kwargs):
        """Exports project files to Alembic / FBX / USD

        Called from within the UI

        Args:
            parent (QtCore.QObject): Parent object
            task_id (str): Task ID 
        """        
        return False

    def on_publish(self, **kwargs):
        """Publish working files and project files for task

        Called from within the UI

        Args:
            parent (QtCore.QObject): Parent object
            project (dict): Kitsu Project Entity
            task_id (str): Task ID 
            task_types (list): Optional - Task types to include in search or none for all
            status_types (list): Optional - Status types to include in search or none for all            
        """        
        return False

    def on_playblast(self, **kwargs):
        return False

    def on_entity_info(self, **kwargs):
        return False

    def on_export2(self, **kwargs):
        # exports to fbx file
        pass
        '''
        source = kwargs["target"]
        working_dir = kwargs["working_dir"]

        self.log_output("calling fbx export {0} {1}".format(source, working_dir))

        target = os.path.join(working_dir, source)
        target = os.path.normpath(target)        

        cmds.FBXExport('-file', target, '-s')
        ##self.log_output("fbx_export", kwargs)
        return True
        '''

    def load_project_episodes(self):
        # self.log_output("load_project_episodes")

        return ProjectEpisodeLoader().run()

    def load_project_shots(self, episode_id):
        # self.log_output("load_project_shots")

        return ProjectShotLoader(episode_id).run()        

    def load_todo_tasks(self, project_id, episode_id):
        # self.log_output("load_todo_tasks")

        return ToDoLoader(project_id, episode_id).run()     

    def load_task_types(self):

        return TaskTypeLoader(self).run()      

    def validate_connection(self):
        # self.log_output("validate_connection")

        settings = SwingSettings.get_instance()
        return connect_to_server(settings.swing_user(), settings.swing_password())

    def get_task_sections(self, task):
        sections = []
        if "project" in task:
            if "code" in task["project"] and task["project"]["code"] and len(task["project"]["code"]) > 0:
                sections.append(task["project"]["code"])
            else:
                sections.append(task["project"]["name"])

        if "entity_type" in task:
            if task["entity_type"]["name"] == "Shot":
                if "episode" in task:
                    sections.append(task["episode"]["name"])

                if "sequence" in task:
                    sections.append(task["sequence"]["name"])
            else:
                if task["entity_type"]["name"] in StudioInterface.ASSET_TYPE_LOOKUP:
                    sections.append(StudioInterface.ASSET_TYPE_LOOKUP[task["entity_type"]["name"]])
                else:
                    sections.append(task["entity_type"]["name"])                

        if "entity" in task:
            if "code" in task["entity"] and task["entity"]["code"]  and len(task["entity"]["code"]) > 0:
                sections.append(task["entity"]["code"])
            else:
                sections.append(task["entity"]["name"])                 

        if "task_type" in task:
            if "short_name" in task["task_type"]  and task["task_type"]["short_name"] and len(task["task_type"]["short_name"]) > 0:
                sections.append(task["task_type"]["short_name"])
            else:
                sections.append(task["task_type"]["name"])            
        return sections
        #return friendly_string("_".join(sections).lower())        