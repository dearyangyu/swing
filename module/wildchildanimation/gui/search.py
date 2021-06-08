# -*- coding: utf-8 -*-

import traceback
import sys
import os
import re

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

from wildchildanimation.gui.background_workers import *
from wildchildanimation.gui.swing_utils import *

from wildchildanimation.gui.search_files_dialog import Ui_SearchFilesDialog

from wildchildanimation.gui.swing_tables import human_size
from wildchildanimation.gui.downloads import *

TEST_MISSING = [
    'sq00_sh00_layout/hby_e00_sq00_sh00_layout.mb',
    'hby_launchpad_mastermesh_02',
    'hby_character_flower_small_rig_v003.ma{13}',
    'C:/Users/Saloni/Desktop/HB2/season_02/layout_main/assets/props/hby_prop_cloud_proxy_v001.ma{4}'
]

class SearchFilesDialog(QtWidgets.QDialog, Ui_SearchFilesDialog):

    working_dir = None
    
    def __init__(self, project_nav, handler):
        super(SearchFilesDialog, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(640)

        self.nav = project_nav
        self.project = self.nav.get_project()
        self.task_types = self.nav.get_task_types()

        self.handler = handler
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.pushButtonSearch.clicked.connect(self.process)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

    def set_project(self, project):
        self.project = project

    def process(self):
        self.threadpool = QtCore.QThreadPool.globalInstance()

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://example.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        file_list = []

        items = self.textEdit.toPlainText().split(",")
        for i in items:
            file_list.append(i)

        worker = bg.SearchFn(self, edit_api, email, password, file_list, self.project)
        worker.callback.results.connect(self.search_results)

        self.threadpool.start(worker)
        self.enable_ui(False)
    # process        

    def enable_ui(self, enabled):
        self.pushButtonSearch.setEnabled(enabled)
        self.pushButtonCancel.setEnabled(enabled)

        if enabled:
            self.progressBar.setRange(0, 1)
        else:
            # set progressbar to busy
            self.progressBar.setRange(0, 0)

    def search_results(self, file_list):
        self.enable_ui(True)

        if len(file_list) == 0:
            QtWidgets.QMessageBox.information(self, 'File Search', 'No files found, sorry', QtWidgets.QMessageBox.Ok)            
            return                 

        dialog = DownloadDialogGUI(self, self.nav, self.entity, file_list)
        #dialog.load_files(file_list)
        dialog.show()            

    def close_dialog(self):
        self.close()     

