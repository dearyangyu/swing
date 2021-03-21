# -*- coding: utf-8 -*-
#
# Studio Handler callback methods from Treehouse Swing
#
import os
import sys
import traceback

import urllib2, shutil, zipfile

from datetime import datetime

_maya_loaded = False    
try:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMaya as om
    import maya.OpenMayaUI as omui

    import pymel.core as pm
    from pymel.util import putEnv
    _maya_loaded = True
except:
    print("Maya not found")

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    qtMode = 1    

class StudioHandler(QtCore.QObject):

    VERSION = "0.0.2"
    SUPPORTED_TYPES = [".ma", ".mb", ".fbx", ".obj", ".mov", ".mp4", ".wav", ".jpg", ".png" ]

    def __init__(self):
        super(StudioHandler, self).__init__()
        self.log_output("Maya Found: {0}, QtMode: {1}".format(_maya_loaded, qtMode))

    def log_error(self, text):
        if _maya_loaded:
            om.MGlobal.displayError("[StudioHandler] {0}".format(text))
        write_log("[error] {}".format(text))

    def log_warning(self, text):
        if _maya_loaded:
            om.MGlobal.displayWarning("[StudioHandler] {0}".format(text))
        write_log("[warn] {}".format(text))

    def log_output(self, text):
        if _maya_loaded:
            om.MGlobal.displayInfo(text)
        write_log("[info] {}".format(text))    

    def set_globals(self, **kwargs):
        write_log("on_globals")

        if "project" in kwargs:
            putEnv("project", kwargs["project"])

        if "episode" in kwargs:
            putEnv("episode", kwargs["episode"])

        if "sequence" in kwargs:
            putEnv("sequence", kwargs["sequence"])

        if "task_type_name" in kwargs:
            putEnv("task_type_name", kwargs["task_type_name"])

        if "shot" in kwargs:
            putEnv("shot", kwargs["shot"])

        if "asset" in kwargs:
            putEnv("asset", kwargs["asset"])

        if "frame_in" in kwargs:
            putEnv("frame_in", kwargs["frame_in"])

        if "frame_out" in kwargs:
            putEnv("frame_out", kwargs["frame_out"])

        if "frame_count" in kwargs:
            putEnv("frame_count", kwargs["frame_count"])

        return True

    #
    # returns a list of unresolved files in a scene
    def list_unresolved(self):
        self.log_output("searching for unresolved references")
        refs = cmds.file(query = True, list = True, unresolvedName = True)

        self.log_output("searching for unresolved references {}".format(refs))
        return refs

    # tries to import the file specified in source into the currently open scene
    def import_reference(self, **kwargs):
        source = kwargs["source"]
        working_dir = kwargs["working_dir"]
        namespace = kwargs["namespace"]

        self.log_output("Importing {0} to {1}".format(source, working_dir))

        filename, file_extension = os.path.splitext(source)

        if file_extension in StudioHandler.SUPPORTED_TYPES:
            self.log_output("Importing file {}".format(source))

            prompt_val = cmds.file(prompt=True, q=True)
            try:
                cmds.file(source, prompt = False, reference = True, ignoreVersion = True, namespace = namespace, options = "v=0;")
                self.log_output('cmds.file({0}, prompt = False, reference = True, ignoreVersion = True, namespace = {1}, options = "v=0;"'.format(source, namespace))
            except:
                traceback.print_exc(file=sys.stdout)
                self.log_error("Error processing importing reference {}".format(source))
                return False
            finally:
                cmds.file(prompt = prompt_val)

        else:
            self.log_error("File extension not valid {0}".format(file_extension))

        write_log("import_reference complete")
        return True

    # tries to import the file specified in source into the currently open scene
    def load_file(self, **kwargs):
        source = kwargs["source"]
        working_dir = kwargs["working_dir"]

        self.log_output("Loading {0} to {1}".format(source, working_dir))

        filename, file_extension = os.path.splitext(source)

        if file_extension in StudioHandler.SUPPORTED_TYPES:
            self.log_output("Loading file {}".format(source))
            try:
                pm.system.importFile(source)
                self.log_output("importFile {} successfully".format(filename))
            except:
                traceback.print_exc(file=sys.stdout)
                self.log_error("Error processing load file {}".format(source))
                return False
        else:
            self.log_error("File extension not valid {0}".format(file_extension))                

        write_log("load_file complete")
        return True        

    def on_save(self, **kwargs):
        file_path = cmds.file(q = True, sn = True)
        file_base = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(file_base)

        request = {
            "source": file_base,
            "file_path": file_path,
            "file_name": file_name,
            "file_ext": file_ext,            
        }
        return request

    def create_folder(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    # create a new maya project file
    def on_create(self, **kwargs):
        source = kwargs["source"]
        working_dir = kwargs["working_dir"]
        target = os.path.join(working_dir, source)
        target = os.path.normpath(target)

        self.log_output("on_create start {} {} {}".format(source, working_dir, target))
        try:
            # check if there are unsaved changes
            fileCheckState = cmds.file(q=True, modified=True)

            # if there are, save them first ... then we can proceed
            if fileCheckState:
                # pm.confirmDialog(title='Please save your project', message='Please save your project before using Swing', button=['Ok'], defaultButton='Ok', cancelButton='Ok', dismissString='Ok')
                # return False
                self.log_output("on_create::saving scene")
                # This is maya's native call to save, with dialogs, etc.
                # No need to write your own.
                cmds.SaveScene()

            if not os.path.exists(working_dir):
                os.makedirs(working_dir)

            mel.eval('setProject "{}"'.format(working_dir))
            cmds.file(new=True, force=True)
            cmds.file(rename=source)
            cmds.file(save=True)
            return True
        except:
            traceback.print_exc(file=sys.stdout)
            self.log_error("Error creating file {}".format(source))

        self.log_output("on_create complete")

    def on_playblast(self, **kwargs):
        self.log_output("on_playblast", kwargs)
        return False
        # playblast  -format avi -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;


def write_log(*args):
    log = "# {} : swing".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    print(log)
