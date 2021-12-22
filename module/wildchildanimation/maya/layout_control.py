# -*- coding: utf-8 -*-
import sys
import traceback
import glob

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    qtMode = 1

import maya.utils as mutils    


from wildchildanimation.maya.layout_control_dialog import Ui_LayoutDialog
from wildchildanimation.gui.file_select_dialog import FileListDialog

'''
    Ui_LayoutControlDialog class
    ################################################################################
'''

class LayoutControlDialog(QtWidgets.QDialog, Ui_LayoutDialog):

    def __init__(self, parent, handler, task):
        super(LayoutControlDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler
        self.task = task

        self.pushButtonChainsaw.clicked.connect(self.run_chainsaw)
        self.pushButtonAnimPrep.clicked.connect(self.run_anim_prep)

        self.pushButtonClose.clicked.connect(self.close_dialog)

        self.pushButtonTurnover.clicked.connect(self.do_turnover)

    def close_dialog(self):
        self.close()

    def run_chainsaw(self):
        try:
            mutils.executeDeferred(lambda: self.do_chainsaw())
            #swing_loader = SwingLoader(self.handler)
            #self.threadpool.start(swing_loader)
            # 
        except:
            self.workspace_control_instance.log_output("chainsaw:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def run_anim_prep(self):
        break_out_dir = "{}/breakout".format(self.handler.get_scene_path())
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Chainsaw's Breakout Folder", break_out_dir)
        if q:
            file_list = glob.glob("{}/*.ma".format(break_out_dir))
            self.file_select_dialog = FileListDialog(self, file_list)
            self.file_select_dialog.show()
            if self.file_select_dialog.status == 'OK':
                selected = self.file_select_dialog.get_selected()
                for item in selected:
                    print(item)
        try:
            mutils.executeDeferred(lambda: self.do_anim_prep(selected))
            #swing_loader = SwingLoader(self.handler)
            #self.threadpool.start(swing_loader)
            # 
            pass
        except:
            self.workspace_control_instance.log_output("anim_prep:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)            


    def do_chainsaw(self):
        # def chainsaw(self, csv_filename, file_prefix = "hby_204_", shot_start = 10, shot_step = 10):

        scene_name = self.handler.get_scene_name()
        if 'untitled' in scene_name:
            print("Error: Can not work on unsaved scenes {}".format(scene_name))
            return False

        if not self.task:
            print("Error: No task found to to process")
            return False

        #project = self.task["project"]
        #if "code" in project and len(project["code"]) > 0:
        #    prefix = project["code"]
        #else:
        #    prefix = project["name"]

        working_dir = self.handler.get_scene_path()
        if not working_dir or len(working_dir) <= 0:
            print("Error: Working dir {} is invalid".format(working_dir))
            return False

        csv_file = "{}.csv".format(scene_name)

        print("ChainSaw: Scene: {} using dir {} into {}".format(scene_name,  working_dir, csv_file))
        
        try:
            if self.handler.chainsaw(csv_file):
                QtWidgets.QMessageBox.information(self, 'Swing: Layout', 'Finished exporting shots')               

        except:
            print("Error in chainsaw ...")
            traceback.print_exc(file=sys.stdout)

    def do_anim_prep(self, list_of_files):
        '''
        maya -batch -c “xxx” -f filename1.mb
        '''
        maya_cmd = "C:/Program Files/Autodesk/Maya2022/bin/maya.exe"
        maya_cmd += " -batch"
        maya_cmd += " -c `from wildchildanimation.studio.maya_studio_handlers import MayaStudioHandler\r\nMayaStudioHandler().anim_prep()` "

        for item in list_of_files:
            cmd = "{} -f {}".format(maya_cmd, item)
            print(cmd)

    def do_turnover(self):
        pass
