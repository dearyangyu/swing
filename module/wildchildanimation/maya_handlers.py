# -*- coding: utf-8 -*-
#
# Studio Handler callback methods from Treehouse Swing
#
import os
import csv
import sys
import traceback

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

from wildchildanimation.studio_interface import StudioInterface
from wildchildanimation.gui.swing_playblast import *
from wildchildanimation.maya.swing_shelf import SwingShelf

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class StudioHandler(StudioInterface):

    NAME = "MayaSwingInterface"
    VERSION = "0.0.3"
    SUPPORTED_TYPES = [".ma", ".mb", ".fbx", ".obj", ".mov", ".mp4", ".wav", ".jpg", ".png" ]

    def __init__(self):
        super(StudioHandler, self).__init__()
        self.log_output("Maya Found: {0}".format(_maya_loaded))

    # populates maya shelf
    def build_shelf(self, swing_gui):
        SwingShelf(controller = swing_gui, name = "Wild_Child", iconPath = "{}/resources/".format(os.path.dirname(os.path.realpath(__file__))))

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

    def get_param(self, option, value):
        ### runs a custom value request against the local dcc
        if option == "frame_range":

            if value == "Render":
                start_frame = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
                end_frame = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
            elif value == "Playback":
                start_frame = int(cmds.playbackOptions(q=True, minTime=True))
                end_frame = int(cmds.playbackOptions(q=True, maxTime=True))
            elif value == "Animation":
                start_frame = int(cmds.playbackOptions(q=True, animationStartTime=True))
                end_frame = int(cmds.playbackOptions(q=True, animationEndTime=True))
            else:
                raise RuntimeError("Invalid frame range preset: {0}".format(value))

            return (start_frame, end_frame)

        raise None
        

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

    #
    #
    # Exports the scene in layout format
    #
    # Source: Chainsaw002.py
    # Author: Miruna D. Mateescu
    # Last Modified: 2021/04/05
    #
    def export_to_csv(csv_filename, file_prefix = "hby_204_", shot_start = 10, shot_step = 10):
        all_shots = cmds.ls(type="shot")
        shot_no = shot_start        
        with open(csv_filename, 'w') as csv_file:
            writer = csv.writer(csv_file)            
            for crt_shot in all_shots:
                shot_start = cmds.getAttr(crt_shot+".startFrame")
                shot_end = cmds.getAttr(crt_shot+".endFrame")
                shot_cam = cmds.listConnections(crt_shot+".currentCamera")                
                cmds.playbackOptions(animationStartTime=shot_start, minTime=shot_start, animationEndTime=shot_end, maxTime=shot_end)
                cmds.lookThru(shot_cam)
                cmds.currentTime(shot_start)                
                if "shot_" in crt_shot:
                    if shot_no < 100:
                        padding = "0"
                    else:
                        padding = ""                    
                    shot_name = "SH"+padding+str(shot_no)
                    cmds.rename(crt_shot, shot_name)
                    cmds.file(rn=file_prefix+shot_name+".ma")
                    cmds.file(save=True)                    
                    writer.writerow([shot_name, shot_start, shot_end, shot_cam])
                    shot_no += shot_step

    # tries to import the file specified in source into the currently open scene
    def load_file(self, **kwargs):
        source = kwargs["source"]
        force = kwargs["force"]
        working_dir = kwargs["working_dir"]

        self.log_output("load_file:: {0} to {1}".format(source, working_dir))
        self.log_output("Source  {0}".format(working_dir))
        self.log_output("Working Dir {0}".format(working_dir))

        filename, file_extension = os.path.splitext(source)

        if file_extension in StudioHandler.SUPPORTED_TYPES:
            prompt_val = cmds.file(prompt=True, q=True)
            try:
                if not force and cmds.file(q = True, modified = True):
                    if QtWidgets.QMessageBox.question(self, 'Unsaved changes', 'Current scene has unsaved changes. Continue?') == QtWidgets.QMessageBox.StandardButton.Yes:
                        force = True
                    else:
                        self.log_output("Aborted load file")
                        return

                cmds.file(source, open = True, ignoreVersion = True, prompt = False, force = force)
            except:
                traceback.print_exc(file=sys.stdout)
                self.log_error("Error processing importing reference {}".format(source))
                return False
            finally:
                cmds.file(prompt = prompt_val)

        else:
            self.log_error("File extension not valid {0}".format(file_extension))                

        write_log("load_file complete")
        return True    

    # tries to import the file specified in source into the currently open scene
    def import_file(self, **kwargs):
        source = kwargs["source"]
        working_dir = kwargs["working_dir"]

        self.log_output("import_file:: {0} to {1}".format(source, working_dir))
        self.log_output("Source  {0}".format(working_dir))
        self.log_output("Working Dir {0}".format(working_dir))

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

    # tries to import the file specified in source into the currently open scene
    def import_reference(self, **kwargs):
        source = kwargs["source"]
        working_dir = kwargs["working_dir"]
        namespace = kwargs["namespace"]

        self.log_output("load_reference:: {0}".format(source, working_dir))
        self.log_output("Source  {0}".format(working_dir))
        self.log_output("Working Dir {0}".format(working_dir))
        self.log_output("Namespace {0}".format(namespace))

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
            cmds.file(save=True, type='mayaAscii')
            return True
        except:
            traceback.print_exc(file=sys.stdout)
            self.log_error("Error creating file {}".format(source))

        self.log_output("on_create complete")

    def on_playblast(self, **kwargs):
        dialog = SwingPlayblastUi()
        dialog.show()

        self.log_output("open: playblast")
        return True
        # playblast  -format avi -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;

    def fbx_export(self, **kwargs):
        # exports current selected
        source = kwargs["target"]
        working_dir = kwargs["working_dir"]
        selection = kwargs["selection"]

        target = os.path.join(working_dir, source)
        target = os.path.normpath(target)       

        if "All" in selection:
            # select all dag objects and all dependency nodes
            pm.select(all = True) 

        # https://tech-artists.org/t/solved-problem-exporting-fbx-from-maya-without-animation/8796        
        cmds.FBXResetExport()
        cmds.FBXExportHardEdges('-v', True)
        cmds.FBXExportSmoothingGroups('-v', True)
        cmds.FBXExportTangents('-v', True)
        cmds.FBXExportBakeComplexAnimation('-v', True)

        cmds.FBXExport('-file', target, '-s')

        self.log_output("fbx export {0} {1}".format(source, working_dir))        
        return True

def write_log(*args):
    log = "# {} : swing".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    print(log)
