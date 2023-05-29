# -*- coding: utf-8 -*-
# Unreal Service Controller
# Entry point for calling UE specific functions

import sys
import unreal

from wildchildanimation.studio.studio_interface import StudioInterface
from wildchildanimation.unreal.gui.shot_selector_dialog import *
from wildchildanimation.unreal.unreal_asset_manager import *

try:
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtWidgets
    qtMode = 1 

# === theme it dark
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False    

global window    

class UnrealStudioHandler(StudioInterface):

    NAME = "UnrealStudioHandler"
    VERSION = "0.0.6"      

    def __init__(self):
        super(UnrealStudioHandler, self).__init__()
        ## self.log_output("Loaded: {} {}".format(UnrealStudioHandler.NAME, UnrealStudioHandler.VERSION))  
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
        app = None

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()

        if darkStyle:
            app.setStyleSheet(qdarkstyle.load_stylesheet())
        # global window

        dlg_instance = ShotSelectorDialog()

        unreal.parent_external_window_to_slate(dlg_instance.winId())
        dlg_instance.exec_()
        return True    
    
    #
    # Load and Spawn Static Mesh using JSON spec file
    #
    def on_asset_loader(self, **kwargs):
        app = None

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()

        if darkStyle:
            app.setStyleSheet(qdarkstyle.load_stylesheet())
        # global window

        dlg_instance = UnrealAssetManager()

        unreal.parent_external_window_to_slate(dlg_instance.winId())
        dlg_instance.exec_()
        return True        
