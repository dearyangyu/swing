# -*- coding: utf-8 -*-

import traceback
import sys
import os
import re
import json

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance 
    import PySide2.QtUiTools as QtUiTools
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    import sip
    qtMode = 1

from datetime import datetime

from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.dcc_tools_dialog import Ui_DCCToolsDialog

from wildchildanimation.gui.media_info import *

from wildchildanimation.studio_interface import StudioInterface

'''
    DCC Tools class
    ################################################################################
'''

class DCCToolsDialog(QtWidgets.QDialog, Ui_DCCToolsDialog):

    working_dir = None
    
    def __init__(self, parent = None, handler = None, selection = None):
        super(DCCToolsDialog, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler
        self.selection = selection

        if self.selection:
            self.lineEditEntityName.setText(friendly_string(self.selection["name"]))
        else:
            self.lineEditEntityName.setText("Export FBX")

        self.pushButtonFbxExport.clicked.connect(self.fbx_export)
        self.pushButtonDialog.clicked.connect(self.close_dialog)
        self.setupCombo()

    def setupCombo(self):
        self.comboBoxFrameRange.clear()

        for item in StudioInterface.FRAME_RANGE_PRESETS:
            self.comboBoxFrameRange.addItem(item)

        self.comboBoxFrameRange.currentIndexChanged.connect(self.frame_range_change)

    def frame_range_change(self, index):
        frame_range = self.comboBoxFrameRange.currentText()
        self.set_frame_range(frame_range)

    def close_dialog(self):
        self.close()

    def set_frame_range(self, frame_range):
        resolved_frame_range = self.resolve_frame_range(frame_range)
        if not resolved_frame_range:
            return

        self._frame_range_preset = None
        if frame_range in StudioInterface.FRAME_RANGE_PRESETS:
            self._frame_range_preset = frame_range

        self._start_frame = resolved_frame_range[0]
        self.spinBoxStart.setValue(self._start_frame)

        self._end_frame = resolved_frame_range[1]
        self.spinBoxEnd.setValue(self._start_frame)

    def get_start_end_frame(self):
        if self._frame_range_preset:
            return self.preset_to_frame_range(self._frame_range_preset)

        return (self._start_frame, self._end_frame)

    def resolve_frame_range(self, frame_range):
        try:
            if type(frame_range) in [list, tuple]:
                start_frame = frame_range[0]
                end_frame = frame_range[1]
            else:
                start_frame, end_frame = self.preset_to_frame_range(frame_range)

            return (start_frame, end_frame)

        except:
            presets = []
            for preset in StudioInterface.FRAME_RANGE_PRESETS:
                presets.append("'{0}'".format(preset))
            ## self.log_error('Invalid frame range. Expected one of (start_frame, end_frame), {0}'.format(", ".join(presets)))

        return None

    def preset_to_frame_range(self, frame_range_preset):
        if "Custom" in frame_range_preset:
            return (self.spinBoxStart.value(), self.spinBoxEnd.value())

        if not self.handler:
            return False        

        return self.handler.get_param("frame_range", frame_range_preset)

    def fbx_export(self):
        if not self.handler:
            return False

        try:
            if self.selection:
                export = "{0}.fbx".format(friendly_string(self.selection["name"]))
            else:
                export = "fbx.fbx"

            working_dir = load_settings("last_fbx", os.path.expanduser("~"))
            selection = self.comboBoxFbxSelection.currentText()


            default_name = os.path.normpath(os.path.join(working_dir, export))
            fbx_file = QtWidgets.QFileDialog.getSaveFileName(self, caption = 'Export FBX as', dir = default_name, filter = "fbx (*.fbx);;All files (*.*)")

            if not fbx_file or fbx_file[0] == '':
                return False

            save_settings("last_fbx", os.path.dirname(fbx_file[0]))                

            self.handler.fbx_export(target = fbx_file[0], working_dir = working_dir, selection = selection)
        except:
            traceback.print_exc(file=sys.stdout)           

    def playblast_scene(self):
        if not self.handler:
            return False

        self.handler.on_playblast()
        self.close_dialog()
        
        '''
        # call maya handler: import into existing workspace
        if self.handler:
            self.append_status("Running handlers")
            try:
                if (self.handler.on_playblast(source = file_name, working_dir = working_dir)):
                    self.append_status("Playblast done")
                else:
                    self.append_status("Playblast error", True)
            except:
                traceback.print_exc(file=sys.stdout)          
        else:
            self.append_status("Maya handler not loaded")


        self.append_status("{}".format(message))        
        '''            

