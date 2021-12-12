# -*- coding: utf-8 -*-
import sys
import traceback

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    qtMode = 1


from wildchildanimation.maya.breakout_control_dialog import Ui_BreakOutDialog

'''
    Ui_BreakoutControlDialog class
    ################################################################################
'''

class BreakoutControlDialog(QtWidgets.QDialog, Ui_BreakOutDialog):

    def __init__(self, parent, handler, task):
        super(BreakoutControlDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler
        self.task = task

        self.pushButtonClose.clicked.connect(self.close_dialog)

        self.pushButtonChainsaw.clicked.connect(self.do_chainsaw)
        self.pushButtonAnimPrep.clicked.connect(self.do_anim_prep)
        self.pushButtonTurnover.clicked.connect(self.do_turnover)

    def close_dialog(self):
        self.close()

    def do_chainsaw(self):
        # def chainsaw(self, csv_filename, file_prefix = "hby_204_", shot_start = 10, shot_step = 10):

        scene_name = self.handler.get_scene_name()
        if 'untitled' in scene_name:
            print("Error: Can not work on unsaved scenes {}".format(scene_name))
            return False

        if not self.task:
            print("Error: No task found to to process")
            return False

        project = self.task["project"]
        if "code" in project and len(project["code"]) > 0:
            prefix = project["code"]
        else:
            prefix = project["name"]

        working_dir = self.handler.get_scene_path()
        if not working_dir or len(working_dir) <= 0:
            print("Error: Working dir {} is invalid".format(working_dir))
            return False

        shot_start = 10
        shot_step = 10

        csv_file = "{}/{}.csv".format(working_dir, prefix)

        print("ChainSaw: Prefix {} Scene: {} from {} by {} using dir {} into {}".format(prefix, scene_name, shot_start, shot_step, working_dir, csv_file))
        
        ### def chainsaw(self, csv_filename, file_prefix = "hby_204_", shot_start = 10, shot_step = 10):
        try:
            self.handler.chainsaw(csv_file, "{}_".format(prefix), shot_start, shot_step)
        except:
            print("Error in chainsaw ...")
            traceback.print_exc(file=sys.stdout)

    def do_anim_prep(self):
        pass

    def do_turnover(self):
        pass
