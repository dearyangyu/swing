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
    log = "{}: SWING".format(datetime.now().strftime("%d/%m%Y %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    print(log)

class StudioHandler():

    def on_globals(self, **kwargs):
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

  

    # tries to import the file specified in source into the currently open scene
    def on_import(self, **kwargs):
        write_log("on_import")

        source = kwargs["source"]
        working_dir = kwargs["working_dir"]

        filename, file_extension = os.path.splitext(source)
        
        if file_extension in [ ".ma", ".mb", ".fbx", ".obj" ]:
            write_log("Importing {}".format(filename))
            try:
                pm.system.importFile(source)
                write_log("Imported {}".format(filename))
            except:
                traceback.print_exc(file=sys.stdout)
                write_log("Error importing file {}".format(source))              

        write_log("on_import_file complete")

    def create_folder(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    # tries to import the file specified in source into the currently open scene
    def on_create(self, **kwargs):
        # file -f -new;
        write_log("on_create")

        source = kwargs["source"]
        working_dir = kwargs["working_dir"]

        pm.system.newFile()


    def on_playblast(self, **kwargs):
        write_log("on_playblast", kwargs)
        # playblast  -format avi -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;

# source = "C:\Users\User\Documents\hby\shots\E00\SQ00\SH00\hby_titleText_mastermesh.ma"
# working_dir = "C:\Users\User\Documents\hby\shots\E00\SQ00\SH00"
# StudioHandler().on_import_file(source, working_dir)
