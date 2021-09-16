# -*- coding: utf-8 -*-
# 
import os
import sys
import traceback
from wildchildanimation.gui.downloads import DownloadDialogGUI
from wildchildanimation.gui.loader import LoaderDialogGUI
from wildchildanimation.gui.publish import PublishDialogGUI

from wildchildanimation.gui.swing_create import SwingCreateDialog
from wildchildanimation.studio.studio_interface import StudioInterface

from wildchildanimation.gui.search import SearchFilesDialog
from wildchildanimation.gui.entity_info import EntityInfoDialog

from wildchildanimation.gui.swing_utils import write_log

try:
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtWidgets
    qtMode = 1 

class SwingStudioHandler(StudioInterface):

    NAME = "SwingStudioHandler"
    VERSION = "0.0.5"      

    def __init__(self):
        super(SwingStudioHandler, self).__init__()
        ## self.log_output("Loaded: {} {}".format(SwingStudioHandler.NAME, SwingStudioHandler.VERSION))  
        # 

    ### Logging functions
    def log_error(self, text):

        write_log("{}::ERROR {}".format(self.NAME, text))

    def log_warning(self, text):

        write_log("{}::WARN {}".format(self.NAME, text))

    def log_output(self, text):

        write_log("{}::{}".format(self.NAME, text))        
    ###

    
    #
    # Swing API Handlers
    #
    def on_create(self, **kwargs):
        parent = kwargs["parent"]
        task = kwargs["task"]

        self.createDialog = SwingCreateDialog(parent, task_id = task["id"], entity_id = task["entity_id"])
        result = self.createDialog.exec_()
        if result:
            working_dir = self.createDialog.get_working_dir()

            # filename, file_extension = os.path.splitext(target)
            # file_name = self.createDialog.get_file_name()
            
            # software = kwargs["software"]
            try:
                os.makedirs(working_dir, exist_ok = True)
                os.startfile(working_dir)
                QtWidgets.QMessageBox.information(self.parent(), 'Swing: Create', 'Created folder {}'.format(working_dir), QtWidgets.QMessageBox.Ok)  
            except:
                traceback.print_exc(file=sys.stdout) 
                return False

        return True    

    def on_publish(self, **kwargs):
        parent = kwargs["parent"]
        task = kwargs["task"] 
        task_types = kwargs["task_types"]
        project_dir = kwargs["project_dir"]
        upload_monitor = kwargs["monitor"]

        self.publishDialog = PublishDialogGUI(parent = parent, task = task, task_types = task_types, upload_monitor = upload_monitor)

        self.publishDialog.set_wf_exclude(StudioInterface.WF_DEFAULT_EXCLUDE)
        self.publishDialog.set_of_include(StudioInterface.OF_DEFAULT_INCLUDE)
        
        if project_dir:
            if os.path.exists(project_dir) and os.path.isdir(project_dir):
                self.publishDialog.set_working_dir(project_dir)
                self.publishDialog.set_output_dir(project_dir)

        self.publishDialog.show()


    def on_load(self, **kwargs):
        parent = kwargs["parent"]
        entity = kwargs["entity"]
        files = kwargs["files"]
        selected = kwargs["selected"]

        loaderDialog = LoaderDialogGUI(parent = parent, handler = self, entity = entity)
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