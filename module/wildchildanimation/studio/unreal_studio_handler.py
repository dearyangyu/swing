# -*- coding: utf-8 -*-
# Unreal Service Controller
# Entry point for calling UE specific functions

import sys
import unreal

from wildchildanimation.studio.studio_interface import StudioInterface
from wildchildanimation.unreal.gui.shot_selector_dialog import *
from wildchildanimation.unreal.unreal_asset_manager import *
from wildchildanimation.unreal.render_submit import *

from wildchildanimation.gui.search import SearchFilesDialog
from wildchildanimation.gui.entity_info import EntityInfoDialog
from wildchildanimation.gui.breakout import BreakoutUploadDialog
from wildchildanimation.gui.downloads import DownloadDialogGUI
from wildchildanimation.gui.swing_render_submit import SwingRenderSubmitDialog

global window    

class UnrealStudioHandler(StudioInterface):

    NAME = "UnrealStudioHandler"
    VERSION = "0.0.10"      

    def __init__(self):
        super(UnrealStudioHandler, self).__init__()

        self.log_output("Loaded: {} {}".format(UnrealStudioHandler.NAME, UnrealStudioHandler.VERSION))  
        # 

    ### Logging functions
    def log_error(self, text):

        unreal.log("{}::ERROR {}".format(self.NAME, text))

    def log_warning(self, text):

        unreal.log("{}::WARN {}".format(self.NAME, text))

    def log_output(self, text):

        unreal.log("{}::{}".format(self.NAME, text))       

    ###
    #
    # API Handlers
    #
    def on_create_shots(self, **kwargs):
        dlg_instance = ShotSelectorDialog()

        #unreal.parent_external_window_to_slate(dlg_instance.winId())
        dlg_instance.exec_()
        return True    
    
    #
    # Load and Spawn Static Mesh using JSON spec file
    #
    def on_asset_loader(self, **kwargs):
        dlg_instance = UnrealAssetManager()

        #unreal.parent_external_window_to_slate(dlg_instance.winId())
        dlg_instance.exec_()
        return True        
    
    #
    # Loads GUI to select render settings and submit to render farm
    #
    def on_render_submit(self, **kwargs):
        dlg_instance = RenderSubmitDialog()

        #unreal.parent_external_window_to_slate(dlg_instance.winId())
        dlg_instance.exec_()
        return True    
    
    def on_render_pub(self, **kwargs):
        parent = kwargs["parent"]
        task = kwargs["task"] 
        project_dir = kwargs["project_dir"]

        self.renderPubDialog = SwingRenderSubmitDialog(parent = parent, task = task)
        self.renderPubDialog.set_working_dir(project_dir)
        self.renderPubDialog.show()

    def on_load(self, **kwargs):
        if len(kwargs) == 0:
            #fixme: find event calling empty kwargs
            return False

        if "parent" in kwargs:
            parent = kwargs["parent"]
        else:
            parent = self

        if "entity" in kwargs:
            entity = kwargs["entity"]
        else:
            entity = None

        if "namespace" in kwargs:
            namespace = kwargs["namespace"]
        else:
            namespace = False            

        files = kwargs["files"]
        selected = kwargs["selected"]

        loaderDialog = LoaderDialogGUI(parent = parent, handler = self, entity = entity, namespace = namespace)
        loaderDialog.load_files(files)
        loaderDialog.set_selected(selected)
        loaderDialog.show()

    def on_search(self, **kwargs):
        parent = kwargs["parent"]
        project = kwargs["project"]
        entity = kwargs["entity"]

        if "text" in kwargs:
            text = kwargs["text"]
        else:
            text = ''

        if "task_types" in kwargs:
            task_types = kwargs["task_types"]
        else:
            task_types = None

        if "status_types" in kwargs:
            status_types = kwargs["status_types"]
        else:
            status_types = None
        
        self.searchDialog = SearchFilesDialog(parent = parent, text = text, entity = entity, project = project, task_types = task_types, status_types = status_types)
        result = self.searchDialog.exec_()
        if result:
            downloadDialog = DownloadDialogGUI(parent = parent, handler = self, file_list = self.searchDialog.get_file_list())
            downloadDialog.show()     

    def on_entity_info(self, **kwargs):
        parent = kwargs["parent"]        
        entity_id = kwargs["entity_id"]
        task_types = kwargs["task_types"]

        dialog = EntityInfoDialog(parent, entity = entity_id, handler = self, task_types = task_types)
        dialog.show()  

    def on_break_out(self, **kwargs):
        project = kwargs["project"]
        episode = kwargs["episode"]
        sequence = kwargs["sequence"]

        dialog = BreakoutUploadDialog(self)
        dialog.set_project(project)
        dialog.set_episode(episode)
        dialog.set_sequence(sequence)

        dialog.exec_()             

