# -*- coding: utf-8 -*-
import sys
import traceback
import glob
import os

import subprocess

from wildchildanimation.gui.maya_sequencer_shot_creator import SequencerShotCreator


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

        self.pushButtonSeqShots.clicked.connect(self.do_camera_xml)
        self.pushButtonChainsaw.clicked.connect(self.run_chainsaw)
        self.pushButtonAnimPrep.clicked.connect(self.run_anim_prep)

        self.pushButtonClose.clicked.connect(self.close_dialog)
        self.pushButtonTurnover.clicked.connect(self.do_turnover)
        self.pushButtonTurnover.setEnabled(False)

    def close_dialog(self):
        self.close()

    def run_chainsaw(self):
        self.pushButtonClose.setEnabled(False)
        #self.progressBar.setMaximum(1)
        try:
            mutils.executeDeferred(lambda: self.do_chainsaw())
        except:
            self.workspace_control_instance.log_output("chainsaw:: {}".format("Exception"))
            traceback.print_exc(file=sys.stdout)

    def do_camera_xml(self):
        if not self.task:
            print("Error: No task found to to process")
            QtWidgets.QMessageBox.information(self, 'Swing::Sequencer Shots', 'Please select a layout task before running Sequencer Shots')               
            return False        

        shotCreator = SequencerShotCreator(self, [], self.handler, self.task)
        shotCreator.show()

    def run_anim_prep(self):
        try:
            break_out_dir = "{}/breakout".format(self.handler.get_scene_path())
        except:
            break_out_dir = os.getcwd()
        # get a directory

        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Chainsaw's Breakout Folder", break_out_dir)
        if q:
            file_list = glob.glob("{}/*.ma".format(q))
            self.file_select_dialog = FileListDialog(self, file_list)
            self.file_select_dialog.exec_()
            if self.file_select_dialog.status == 'OK':
                selected = self.file_select_dialog.get_selected()
                errors = 0
                for item in selected:
                    try:
                        #quoted_item = '"{}"'.format(item)
                        ''' 
                            "C:\Program Files\Autodesk\Maya2022\bin\maya" 
                                -batch
                                -file "C:/Users/pniemandt.STUDIO/Documents/maya/projects/default/productions/aotkb/aotk/user/e001_cat/shots/sc010/sh010/layout/sc010_sh010_layout/breakout\witw_ep101_seq010_sh010.ma" 
                                -command python("\"from wildchildanimation.maya.swing_maya import SwingMaya\nSwingMaya().anim_prep()"\")
                        '''
                        #cmds = []
                        #cmds.append("C:/Program Files/Autodesk/Maya2022/bin/maya.exe")
                        #cmds.append("-batch")
                        #cmds.append("-file")
                        #cmds.append(quoted_item)
                        #cmds.append("-commmand")
                        #cmds.append(''' python("\"from wildchildanimation.maya.swing_maya import SwingMaya\nSwingMaya().anim_prep()"\") ''')

                        cmds = [ "Z:\\env\\wca\\swing\\swing-main\\bin\\anim_prep.bat", item ] 

                        print("Running command: {}".format(str(cmds)))
                        #proc = s
                        subprocess.run(cmds, shell = False, stderr=subprocess.PIPE)
                        print("Completed command: {}".format(str(cmds)))

                        #while True:
                        #    output = proc.stderr.read(1).decode('utf-8')
                        #   if output == '' and proc.poll() != None:
                        #        break
                        #    else:
                        #        sys.stdout.write(output)
                        #        sys.stdout.flush()                        

                        #proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                        #stdout_value = proc.communicate('through stdin to stdout')[0]
                        #print(stdout_value)
                    except:
                        self.workspace_control_instance.log_output("anim_prep:: {}".format("Exception"))
                        traceback.print_exc(file=sys.stdout)   
                        errors += 1
                if errors == 0:
                    QtWidgets.QMessageBox.information(self, 'Swing::Anim Prep', 'Finished anim prep on all shots')                        
                else:
                    QtWidgets.QMessageBox.warning(self, 'Swing::Anim Prep', 'Errors during anim prep, please check generated scene files')                        


    def do_chainsaw(self):
        try:
            scene_name = self.handler.get_scene_name()
            if 'untitled' in scene_name:
                print("Error: Can not work on unsaved scenes {}".format(scene_name))
                QtWidgets.QMessageBox.information(self, 'Swing::Chainsaw', 'Please save the layout scene before running Chainsaw')               
                return False

            if not self.task:
                print("Error: No task found to to process")
                QtWidgets.QMessageBox.information(self, 'Swing::Chainsaw', 'Please select a layout task before running Chainsaw')               
                return False

            working_dir = self.handler.get_scene_path()
            if not working_dir or len(working_dir) <= 0:
                print("Error: Working dir {} is invalid".format(working_dir))
                return False

            csv_file = "{}.csv".format(scene_name)

            print("ChainSaw: Scene: {} using dir {} into {}".format(scene_name,  working_dir, csv_file))
            
            try:
                if self.handler.chainsaw(csv_file):
                    QtWidgets.QMessageBox.information(self, 'Swing::Chainsaw', 'Finished exporting shots')               

            except:
                print("Error in chainsaw ...")
                traceback.print_exc(file=sys.stdout)

                QtWidgets.QMessageBox.warning(self, 'Swing::Chainsaw', 'Errors exporting shots')               
        finally:
            # self.progressBar.setMaximum(0)
            self.pushButtonClose.setEnabled(True)

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
