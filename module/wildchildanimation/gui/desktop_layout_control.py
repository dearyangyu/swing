# -*- coding: utf-8 -*-
import sys
import traceback
import glob
import os

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    qtMode = 1

from wildchildanimation.gui.desktop_layout_control_dialog import Ui_DesktopLayoutDialog
from wildchildanimation.gui.file_select_dialog import FileListDialog
from wildchildanimation.gui.swing_utils import load_settings

'''
    Ui_LayoutControlDialog class
    ################################################################################
'''

class LayoutControlDialog(QtWidgets.QDialog, Ui_DesktopLayoutDialog):

    def __init__(self, parent, handler, project, episode, sequence):
        super(LayoutControlDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler
        self.project = project
        self.episode = episode
        self.sequence = sequence

        self.pushButtonClose.clicked.connect(self.close_dialog)

        self.pushButtonImportXML.clicked.connect(self.import_xml)
        self.pushButtonBreakout.clicked.connect(self.process_breakout)

    def import_xml(self):
        q = QtWidgets.QFileDialog.getOpenFileName(self, "select fcpxml file", load_settings("last_breakout", os.path.expanduser("~")), "FCPXML file (*.xml);;All Files (*.*)")
        if not (q):
            return 

        self.handler.on_load_shot_xml(parent = self, project = self.project, episode = self.episode, sequence = self.sequence, source_xml = q[0])

    def process_breakout(self):
        self.handler.on_break_out(parent = self, project = self.project, episode = self.episode, sequence = self.sequence)


    def close_dialog(self):
        self.close()

