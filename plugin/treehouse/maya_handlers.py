# -*- coding: utf-8 -*-
#
# Studio Handler callback methods from Treehouse Swing
#
import maya.mel as mel
import maya.cmds as cmds

import pymel.core as pm

from pymel.util import putEnv

import os
import sys
import traceback

from datetime import datetime


def write_log(*args):
    log = "# {} : swing".format(datetime.now().strftime("%d/%m%Y %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    print(log)


class StudioHandler():

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

    # tries to import the file specified in source into the currently open scene
    def on_import(self, **kwargs):
        source = kwargs["source"]
        working_dir = kwargs["working_dir"]

        write_log("on_import start", source, working_dir)

        filename, file_extension = os.path.splitext(source)

        if file_extension in [".ma", ".mb", ".fbx", ".obj"]:
            write_log("Importing {}".format(filename))
            try:
                pm.system.importFile(source)
                write_log("Imported {}".format(filename))
            except:
                traceback.print_exc(file=sys.stdout)
                write_log("Error importing file {}".format(source))
                return False

        write_log("on_import_file complete")
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

        write_log("on_create start", source, working_dir, target)
        try:
            # check if there are unsaved changes
            fileCheckState = cmds.file(q=True, modified=True)

            # if there are, save them first ... then we can proceed
            if fileCheckState:
                # pm.confirmDialog(title='Please save your project', message='Please save your project before using Swing', button=['Ok'], defaultButton='Ok', cancelButton='Ok', dismissString='Ok')
                # return False
                write_log("on_create", "saving scene")
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
            write_log("Error creating file {}".format(source))

    write_log("on_create complete")

    def on_playblast(self, **kwargs):
        write_log("on_playblast", kwargs)
        return False
        # playblast  -format avi -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;

# source = "C:\Users\User\Documents\hby\shots\E00\SQ00\SH00\hby_titleText_mastermesh.ma"
# working_dir = "C:\Users\User\Documents\hby\shots\E00\SQ00\SH00"
# StudioHandler().on_import_file(source, working_dir)
